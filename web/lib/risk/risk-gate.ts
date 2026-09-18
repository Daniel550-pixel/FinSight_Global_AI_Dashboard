export type RiskDecision={allowed:boolean;reasons:string[];utilization:number;checks:Record<string,boolean>};
export type RiskInput={side:"buy"|"sell";quantity:number;price:number;position:number;cash:number;equity:number;drawdown:number;atrPct:number;spread:number;imbalance:number;bestBidQuantity:number;bestAskQuantity:number};
export class RiskGate{
 readonly maxPosition=100; readonly maxNotional=500_000; readonly maxOrderQuantity=10; readonly maxDrawdownPct=5; readonly maxAtrPct=5; readonly maxSpreadPct=0.2;
 evaluate(input:RiskInput):RiskDecision{
  const signed=input.side==="buy"?input.quantity:-input.quantity,nextPosition=input.position+signed,notional=Math.abs(nextPosition*input.price),spreadPct=input.price>0?(input.spread/input.price)*100:0;
  const checks={position:Math.abs(nextPosition)<=this.maxPosition,notional:notional<=this.maxNotional,orderSize:input.quantity<=this.maxOrderQuantity,drawdown:input.drawdown<=this.maxDrawdownPct,volatility:input.atrPct<=this.maxAtrPct,liquidity:spreadPct<=this.maxSpreadPct,imbalance:input.side==="buy"?input.imbalance>-0.45:input.imbalance<0.45};
  const reasons:string[]=[]; if(!checks.position)reasons.push("MAX_POSITION"); if(!checks.notional)reasons.push("MAX_NOTIONAL"); if(!checks.orderSize)reasons.push("MAX_ORDER_SIZE"); if(!checks.drawdown)reasons.push("DRAWDOWN_GUARD"); if(!checks.volatility)reasons.push("VOLATILITY_GUARD"); if(!checks.liquidity)reasons.push("SPREAD_GUARD"); if(!checks.imbalance)reasons.push("LIQUIDITY_IMBALANCE");
  const utilization=Math.min(100,Math.max(Math.abs(nextPosition)/this.maxPosition*100,notional/this.maxNotional*100,input.drawdown/this.maxDrawdownPct*100,input.atrPct/this.maxAtrPct*100));
  return{allowed:reasons.length===0,reasons,utilization,checks};
 }
}
