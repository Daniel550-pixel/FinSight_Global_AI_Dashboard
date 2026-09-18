export type StrategyName="Momentum"|"Mean Reversion"|"Breakout"|"VWAP"|"Multi-Factor";
export type StrategySignal={name:StrategyName;side:"buy"|"sell"|null;score:number;reason:string};
export const strategies:Record<StrategyName,{description:string}>={
 Momentum:{description:"Trend and impulse continuation"},
 "Mean Reversion":{description:"Statistical deviation capture"},
 Breakout:{description:"Range expansion detection"},
 VWAP:{description:"Volume weighted execution"},
 "Multi-Factor":{description:"Composite signal stack"},
};
export function generateStrategySignals(analysis:{score:number;rsi:number;price:number;sma20:number;sma50:number;macd:number;macdSignal:number;volumeRatio:number},name:StrategyName):StrategySignal{
 let score=analysis.score,reason="Composite market state";
 if(name==="Momentum"){score=Math.round((analysis.macd>analysis.macdSignal?1:-1)*Math.abs(analysis.score));reason="MACD and trend alignment";}
 if(name==="Mean Reversion"){score=Math.round((50-analysis.rsi)*2);reason="RSI distance from equilibrium";}
 if(name==="Breakout"){score=Math.round((analysis.price>analysis.sma20?1:-1)*Math.min(100,Math.abs(analysis.score)+analysis.volumeRatio*5));reason="Price/trend expansion";}
 if(name==="VWAP"){score=Math.round((analysis.price>analysis.sma20?1:-1)*Math.min(100,Math.abs(analysis.score)*.8+analysis.volumeRatio*8));reason="Price and volume participation";}
 if(name==="Multi-Factor"){reason="Trend, momentum, RSI and volume composite";}
 score=Math.max(-100,Math.min(100,score)); return{name,score,reason,side:score>=55?"buy":score<=-55?"sell":null};
}
