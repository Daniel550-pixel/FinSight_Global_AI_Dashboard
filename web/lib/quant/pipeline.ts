import {ExecutionSimulator} from "../execution/simulator";
import {OrderBook,Level} from "../market/order-book";
import {analyzeMarket,MarketAnalysis,Bar} from "../market/indicators";
import {RiskGate,RiskDecision} from "../risk/risk-gate";
import {EventLedger} from "../ledger/event-ledger";
import {generateStrategySignals,StrategyName} from "../strategy/registry";

export class QuantPipeline{
  readonly strategy:StrategyName;
  executor=new ExecutionSimulator(); book=new OrderBook(); riskGate=new RiskGate(); ledger=new EventLedger();
  position=0; cash=100000; realizedPnl=0; events=0; lastPrice=0; avgEntry=0; peakEquity=100000; riskDecision:RiskDecision|null=null; riskEvents=0;
  bars:Bar[]=[]; analysis:MarketAnalysis|null=null; lastBook={bids:[] as Level[],asks:[] as Level[]};

  constructor(strategy:StrategyName="Multi-Factor"){this.strategy=strategy;}

  onBar(e:{symbol:string;timestamp:number;price:number;payload?:Record<string,any>}){
    this.events++;
    const p=e.payload||{},o=Number(p.open??e.price),h=Number(p.high??e.price),l=Number(p.low??e.price),c=Number(p.close??e.price),v=Number(p.volume??0); this.lastPrice=c;
    this.bars.push({time:e.timestamp,open:o,high:h,low:l,close:c,volume:v}); if(this.bars.length>240)this.bars.shift();

    const tick=Math.max(c*0.00005,Math.abs(h-l)*0.08||c*0.00005),levels=10,bids:Level[]=[],asks:Level[]=[];
    for(let i=0;i<levels;i++){const bid=c-tick*(i+1),ask=c+tick*(i+1),base=20+(v%700)/35+i*3;bids.push({price:bid,quantity:Math.max(1,base+(i%3)*8)});asks.push({price:ask,quantity:Math.max(1,base*0.9+(i%4)*7)});}
    this.book.snapshot(bids,asks,e.timestamp,this.events); this.lastBook=this.book.depth(10);
    this.ledger.append(e.timestamp,"market",e.symbol,{close:c,volume:v,mid:this.book.mid(),spread:this.book.spread()});

    this.analysis=this.bars.length>=20?analyzeMarket(this.bars):null;
    if(this.analysis){
      const a=addStrategyInput(this.analysis);
      const strategySignal=generateStrategySignals(a,this.strategy);
      this.ledger.append(e.timestamp,"strategy",e.symbol,{strategy:this.strategy,score:strategySignal.score,side:strategySignal.side,reason:strategySignal.reason,regime:this.analysis.regime});
      const signal=strategySignal.side;
      if(signal&&Math.abs(this.position)<this.riskGate.maxPosition){
        const q=1,equity=this.cash+this.position*c; this.peakEquity=Math.max(this.peakEquity,equity);
        const drawdown=this.peakEquity>0?Math.max(0,(this.peakEquity-equity)/this.peakEquity*100):0;
        this.riskDecision=this.riskGate.evaluate({side:signal,quantity:q,price:c,position:this.position,cash:this.cash,equity,drawdown,atrPct:this.analysis.atrPct,spread:this.book.spread()??0,imbalance:this.book.imbalance(5),bestBidQuantity:this.lastBook.bids[0]?.quantity??0,bestAskQuantity:this.lastBook.asks[0]?.quantity??0});
        this.riskEvents++;
        this.ledger.append(e.timestamp,"risk",e.symbol,{allowed:this.riskDecision.allowed,reasons:this.riskDecision.reasons,utilization:this.riskDecision.utilization});
        if(!this.riskDecision.allowed)return{signal,risk:this.riskDecision,fills:[],analysis:this.analysis,strategySignal};
        this.ledger.append(e.timestamp,"order",e.symbol,{side:signal,quantity:q,type:"market",strategy:this.strategy});
        this.executor.submit(e.symbol,signal,q,undefined,"market");
        const fills=this.executor.processBar(e.symbol,e.timestamp,o,h,l,c); for(const f of fills)this.applyFill(f);
        return{signal,risk:this.riskDecision,fills,analysis:this.analysis,strategySignal};
      }
      return{signal:signal??"hold",risk:null,fills:[],analysis:this.analysis,strategySignal};
    }
    return{signal:"hold",risk:null,fills:[],analysis:this.analysis,strategySignal:null};
  }

  private applyFill(f:{timestamp:number;symbol:string;side:"buy"|"sell";price:number;quantity:number;fee:number;orderId:number}){
    const signed=f.side==="buy"?f.quantity:-f.quantity,oldPosition=this.position;
    if(oldPosition===0)this.avgEntry=f.price; else if(Math.sign(oldPosition)===Math.sign(signed))this.avgEntry=(Math.abs(oldPosition)*this.avgEntry+Math.abs(signed)*f.price)/(Math.abs(oldPosition)+Math.abs(signed)); else {const closing=Math.min(Math.abs(oldPosition),Math.abs(signed));this.realizedPnl+=(f.side==="sell"?1:-1)*closing*(f.price-this.avgEntry);if(Math.abs(signed)>Math.abs(oldPosition))this.avgEntry=f.price;}
    this.position+=signed; this.cash-=signed*f.price; this.cash-=f.fee; this.realizedPnl-=f.fee;
    this.ledger.append(f.timestamp,"fill",f.symbol,{orderId:f.orderId,side:f.side,price:f.price,quantity:f.quantity,fee:f.fee});
    this.ledger.append(f.timestamp,"portfolio",f.symbol,{position:this.position,cash:this.cash,realizedPnl:this.realizedPnl});
  }

  snapshot(){
    const equity=this.cash+this.position*this.lastPrice;this.peakEquity=Math.max(this.peakEquity,equity);
    const drawdown=this.peakEquity>0?Math.max(0,(this.peakEquity-equity)/this.peakEquity*100):0,unrealized=this.position?(this.lastPrice-this.avgEntry)*this.position:0,exposure=Math.abs(this.position*this.lastPrice);
    return{strategy:this.strategy,position:this.position,cash:this.cash,lastPrice:this.lastPrice,avgEntry:this.avgEntry,realizedPnl:this.realizedPnl,unrealizedPnl:unrealized,equity,peakEquity:this.peakEquity,drawdown,exposure,riskUtilization:this.riskDecision?.utilization??0,riskDecision:this.riskDecision,riskEvents:this.riskEvents,eventsProcessed:this.events,openOrders:this.executor.orders.size,fills:this.executor.fills.length,analysis:this.analysis,orderBook:this.book,depth:this.lastBook,imbalance:this.book.imbalance(5),spread:this.book.spread(),mid:this.book.mid(),microprice:this.book.microprice(),ledger:this.ledger.latest(30)};
  }
}

function addStrategyInput(a:MarketAnalysis){
  return {score:a.score,rsi:a.rsi,price:a.price,sma20:a.price,sma50:a.price,macd:a.macd,macdSignal:a.macdSignal,volumeRatio:a.volumeRatio};
}
