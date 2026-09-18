export type Bar={time:number;open:number;high:number;low:number;close:number;volume:number};
export type MarketAnalysis={
  score:number; regime:"BULLISH"|"BEARISH"|"NEUTRAL"; action:"PAPER BUY"|"PAPER SELL"|"HOLD";
  confidence:number; rsi:number; atrPct:number; pattern:string; macd:number; macdSignal:number;
  price:number; volumeRatio:number; reasons:string[];
};
const finite=(v:number)=>Number.isFinite(v)?v:0;
const mean=(a:number[])=>a.length?a.reduce((s,v)=>s+v,0)/a.length:0;
const sma=(a:number[],n:number)=>mean(a.slice(Math.max(0,a.length-n)));
const ema=(a:number[],n:number)=>{const k=2/(n+1);let e=a[0]??0;for(let i=1;i<a.length;i++)e=a[i]*k+e*(1-k);return e};
export function addIndicators(bars:Bar[]){
  const c=bars.map(x=>x.close),h=bars.map(x=>x.high),l=bars.map(x=>x.low),v=bars.map(x=>x.volume);
  const ema12=ema(c,12),ema26=ema(c,26),macd=ema12-ema26;
  const prevE12=ema(c.slice(0,-1),12),prevE26=ema(c.slice(0,-1),26),prevMacd=prevE12-prevE26;
  const signal=prevMacd+(macd-prevMacd)*(2/10);
  const deltas=c.slice(1).map((x,i)=>x-c[i]);const gains=deltas.map(x=>Math.max(0,x));const losses=deltas.map(x=>Math.max(0,-x));
  const ag=mean(gains.slice(-14)),al=mean(losses.slice(-14));const rsi=al===0?100:100-100/(1+ag/al);
  const trs=bars.map((x,i)=>i?Math.max(x.high-x.low,Math.abs(x.high-c[i-1]),Math.abs(x.low-c[i-1])):x.high-x.low);
  const atr=mean(trs.slice(-14)),price=c.at(-1)??0;
  const row=bars.at(-1)!;const body=Math.abs(row.close-row.open),range=Math.max(row.high-row.low,1e-12);
  const upper=row.high-Math.max(row.open,row.close),lower=Math.min(row.open,row.close)-row.low;
  const pattern=body/range<.12&&lower/range>.55?"Hammer":body/range<.12&&upper/range>.55?"Shooting star":row.close>row.open&&body/range>.65?"Strong bullish candle":row.close<row.open&&body/range>.65?"Strong bearish candle":"Neutral candle";
  const volumeRatio=row.volume/(sma(v,20)||1);
  const high20=Math.max(...h.slice(-21,-1)),low20=Math.min(...l.slice(-21,-1));
  const sma20=sma(c,20),sma50=sma(c,50);
  return {price,sma20,sma50,ema12,ema26,macd,macdSignal:signal,macdHist:macd-signal,rsi,atrPct:price?atr/price*100:0,pattern,volumeRatio,return20:c.length>20?(price/c[c.length-21]-1)*100:0,high20,low20};
}
export function analyzeMarket(bars:Bar[]):MarketAnalysis{
  const x=addIndicators(bars);let score=0;const reasons:string[]=[];
  if(x.sma20>x.sma50){score+=22;reasons.push("20-period trend is above the 50-period trend.")}else{score-=22;reasons.push("20-period trend is below the 50-period trend.")}
  if(x.price>x.sma20){score+=14;reasons.push("Price is holding above the short-term trend.")}else{score-=14;reasons.push("Price is below the short-term trend.")}
  if(x.macd>x.macdSignal){score+=18;reasons.push("MACD momentum is positive.")}else{score-=18;reasons.push("MACD momentum is negative.")}
  if(x.rsi>=58){score+=12;reasons.push("RSI confirms positive momentum.")}else if(x.rsi<=42){score-=12;reasons.push("RSI confirms negative momentum.")}else reasons.push("RSI is neutral.");
  if(x.pattern==="Strong bullish candle"){score+=10;reasons.push("Latest candle shows strong buying pressure.")}else if(x.pattern==="Strong bearish candle"){score-=10;reasons.push("Latest candle shows strong selling pressure.")}else if(x.pattern==="Hammer"){score+=5;reasons.push("Hammer pattern may indicate rejection of lower prices.")}else if(x.pattern==="Shooting star"){score-=5;reasons.push("Shooting-star pattern may indicate rejection of higher prices.")}
  if(x.price>x.high20){score+=12;reasons.push("Price is breaking above the 20-bar range.")}else if(x.price<x.low20){score-=12;reasons.push("Price is breaking below the 20-bar range.")}
  score=Math.max(-100,Math.min(100,Math.round(score)));
  const regime=score>=40?"BULLISH":score<=-40?"BEARISH":"NEUTRAL";const action=score>=55?"PAPER BUY":score<=-55?"PAPER SELL":"HOLD";
  return {score,regime,action,confidence:Math.max(55,Math.min(95,Math.round(55+Math.abs(score)*.42))),rsi:finite(x.rsi),atrPct:finite(x.atrPct),pattern:x.pattern,macd:x.macd,macdSignal:x.macdSignal,price:x.price,volumeRatio:finite(x.volumeRatio),reasons:reasons.slice(-5)};
}
export function analyzeChartType(bars:Bar[],chartType:string){const base=analyzeMarket(bars),x=addIndicators(bars);let extra=0;const reasons=[...base.reasons];
  if(chartType==="Candlestick"){if(["Strong bullish candle","Hammer"].includes(x.pattern)){extra+=12;reasons.push("Candlestick confirmation: "+x.pattern+".")}else if(["Strong bearish candle","Shooting star"].includes(x.pattern)){extra-=12;reasons.push("Candlestick confirmation: "+x.pattern+".")}}
  else if(chartType==="MACD momentum"){if(x.macd>x.macdSignal&&x.macdHist>0){extra+=18;reasons.push("MACD line and histogram confirm positive momentum.")}else if(x.macd<x.macdSignal&&x.macdHist<0){extra-=18;reasons.push("MACD line and histogram confirm negative momentum.")}else reasons.push("MACD signals are mixed.")}
  else if(chartType==="RSI"){if(x.rsi>=52&&x.rsi<=68){extra+=10;reasons.push("RSI is in a constructive momentum zone.")}else if(x.rsi>=70){extra-=8;reasons.push("RSI is overbought; momentum may be stretched.")}else if(x.rsi<=30){extra+=8;reasons.push("RSI is oversold; downside may be exhausted.")}}
  else if(chartType==="Volume"){if(x.volumeRatio>=1.5&&base.score>0){extra+=12;reasons.push(`Volume is elevated at ${x.volumeRatio.toFixed(1)}× its 20-bar average.`)}else if(x.volumeRatio>=1.5&&base.score<0){extra-=12;reasons.push(`Heavy volume confirms selling pressure at ${x.volumeRatio.toFixed(1)}× average.`)}}
  else if(chartType==="Line + trend"){if(x.ema12>x.ema26&&x.price>x.sma20){extra+=14;reasons.push("Short-term trend lines are aligned bullishly.")}else if(x.ema12<x.ema26&&x.price<x.sma20){extra-=14;reasons.push("Short-term trend lines are aligned bearishly.")}}
  const score=Math.max(-100,Math.min(100,base.score+extra));return {...base,score,regime:score>=40?"BULLISH":score<=-40?"BEARISH":"NEUTRAL",action:score>=60?"PAPER BUY":score<=-60?"PAPER SELL":"HOLD",confidence:Math.max(55,Math.min(96,Math.round(55+Math.abs(score)*.42))),reasons:reasons.slice(-6)};
}