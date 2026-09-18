import {MarketAnalysis} from "../market/indicators";
import {StrategyName} from "../strategy/registry";

export type IntelligenceContext={
  symbol:string;
  strategy:StrategyName;
  price:number;
  analysis:MarketAnalysis|null;
  snapshot:any;
  backtest:any;
};

export type IntelligenceResult={
  title:string;
  answer:string;
  facts:string[];
  context:string[];
};

const pct=(n:number)=>`${n>=0?"+":""}${n.toFixed(2)}`;
const money=(n:number)=>`${n>=0?"+":""}$${n.toFixed(2)}`;

export function generateIntelligenceResponse(query:string,ctx:IntelligenceContext):IntelligenceResult{
  const q=query.trim().toLowerCase();
  const a=ctx.analysis;
  const s=ctx.snapshot;
  const regime=a?.regime??"NEUTRAL";
  const signal=s?.ledger?.find((e:any)=>e.type==="strategy")?.data;
  const strategySide=signal?.side??"hold";
  const imbalance=Number(s?.imbalance??0);
  const risk=s?.riskDecision;
  const facts=[
    `${ctx.symbol} price: $${ctx.price.toFixed(2)}`,
    `Regime: ${regime} · score ${a?.score??0}`,
    `Strategy: ${ctx.strategy} · signal ${strategySide.toUpperCase()}`,
    `Order-book imbalance: ${pct(imbalance*100)}%`,
    `Portfolio equity: $${Number(s?.equity??100000).toFixed(2)} · drawdown ${Number(s?.drawdown??0).toFixed(2)}%`,
    `Ledger events: ${s?.eventsProcessed??0} · fills: ${s?.fills??0}`
  ];
  let title="Current terminal state";
  let answer=`The deterministic engine has ${regime.toLowerCase()} regime classification for ${ctx.symbol}. The selected ${ctx.strategy} strategy currently produces a ${strategySide.toUpperCase()} signal. No external market data or LLM inference is used in this explanation.`;
  if(q.includes("risk")){
    title="Risk state";
    answer=`Risk is evaluated from position, equity drawdown, ATR, spread and simulated order-book liquidity. The current gate is ${risk?.allowed?"PASS":"GUARDED"} with utilization ${Number(risk?.utilization??0).toFixed(1)}%. ${(risk?.reasons??[]).join(" ")||"No recorded risk violations."}`;
  }else if(q.includes("strategy")||q.includes("signal")||q.includes("bullish")||q.includes("bearish")||q.includes("why")){
    title=`${ctx.strategy} signal explanation`;
    answer=`The signal is ${strategySide.toUpperCase()} because the strategy consumes the current market score, RSI, MACD structure and volume ratio. Regime is ${regime}; score is ${a?.score??0}; RSI is ${Number(a?.rsi??0).toFixed(1)}; MACD is ${Number(a?.macd??0).toFixed(4)} versus signal ${Number(a?.macdSignal??0).toFixed(4)}; volume ratio is ${Number(a?.volumeRatio??0).toFixed(2)}. The registry reason is: ${signal?.reason??"No strategy signal is available yet."}`;
  }else if(q.includes("execution")||q.includes("fill")||q.includes("order")){
    title="Execution state";
    answer=`The paper execution simulator has ${s?.fills??0} fills and ${s?.openOrders??0} open orders. Current position is ${Number(s?.position??0).toFixed(2)} with average entry ${Number(s?.avgEntry??0).toFixed(2)}. Realized P&L is ${money(Number(s?.realizedPnl??0))} and unrealized P&L is ${money(Number(s?.unrealizedPnl??0))}.`;
  }else if(q.includes("backtest")||q.includes("performance")){
    title="Backtest context";
    answer=ctx.backtest?`${ctx.backtest.strategy} on ${ctx.backtest.symbol} processed ${ctx.backtest.events} events, producing equity $${Number(ctx.backtest.equity).toFixed(2)}, return ${pct(Number(ctx.backtest.returnPct))}%, drawdown ${Number(ctx.backtest.drawdown).toFixed(2)}% and ${ctx.backtest.fills} fills.`:"No backtest has been run in this terminal session.";
  }else if(q.includes("book")||q.includes("liquidity")){
    title="Market microstructure";
    answer=`The simulated book has spread ${Number(s?.spread??0).toFixed(4)}, mid ${Number(s?.mid??ctx.price).toFixed(2)}, microprice ${Number(s?.microprice??ctx.price).toFixed(2)} and imbalance ${pct(imbalance*100)}%. These values describe the deterministic simulation, not a live exchange order book.`;
  }
  return {title,answer,facts,context:["Market analysis","Strategy registry","Order book","Risk gate","Portfolio state","Event ledger",...(ctx.backtest?["Backtest result"]:[])]};
}
