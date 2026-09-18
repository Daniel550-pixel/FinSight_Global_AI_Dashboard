import {ExecutionSimulator} from "../execution/simulator";
import {OrderBook} from "../market/order-book";
import {analyzeMarket,MarketAnalysis,Bar} from "../market/indicators";
export class QuantPipeline{
 executor=new ExecutionSimulator(); book=new OrderBook(); position=0;cash=100000;realizedPnl=0;events=0;lastPrice=0;
 bars:Bar[]=[]; analysis:MarketAnalysis|null=null;
 onBar(e:{symbol:string;timestamp:number;price:number;payload?:Record<string,any>}){
  this.events++;const p=e.payload||{},o=Number(p.open??e.price),h=Number(p.high??e.price),l=Number(p.low??e.price),c=Number(p.close??e.price),v=Number(p.volume??0);
  this.lastPrice=c;this.bars.push({time:e.timestamp,open:o,high:h,low:l,close:c,volume:v});if(this.bars.length>240)this.bars.shift();
  this.analysis=this.bars.length>=20?analyzeMarket(this.bars):null;
  const score=this.analysis?.score??0;const signal=score>=55?"buy":score<=-55?"sell":null;
  if(signal&&Math.abs(this.position)<100){const q=1;this.executor.submit(e.symbol,signal,q,undefined,"market");const fills=this.executor.processBar(e.symbol,e.timestamp,o,h,l,c);for(const f of fills){const signed=f.side==="buy"?f.quantity:-f.quantity;this.position+=signed;this.cash-=signed*f.price;this.cash-=f.fee;this.realizedPnl-=f.fee}return{signal,fills,analysis:this.analysis}}
  return{signal:"hold",fills:[],analysis:this.analysis};
 }
 snapshot(){return{position:this.position,cash:this.cash,lastPrice:this.lastPrice,realizedPnl:this.realizedPnl,equity:this.cash+this.position*this.lastPrice,eventsProcessed:this.events,openOrders:this.executor.orders.size,fills:this.executor.fills.length,analysis:this.analysis}}
}