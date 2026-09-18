import {ReplaySession} from "./replay/session";
import {QuantPipeline} from "./quant/pipeline";
import {StrategyName} from "./strategy/registry";
export function seededBars(symbol:string,n=240,seed=17){
 const profiles:Record<string,[number,number,number]>={SPX:[6481.2,.0001,.01],NDX:[23914.6,.00016,.012],BTC:[113420,.00022,.02],GOLD:[3812.4,.00008,.01],BRENT:[68.7,-.00002,.016],EURUSD:[1.174,.00003,.006]};
 const [base,drift,vol]=profiles[symbol]??[100,.0001,.012]; let x=(seed+symbol.length*97)>>>0,p=base; const bars=[]; const start=Date.UTC(2026,0,2,14,30,0);
 for(let i=0;i<n;i++){x=(x*1664525+1013904223)>>>0;const shock=drift+(x/4294967296-.5)*vol;p*=1+shock;const open=i?p*(1-shock):p/(1+shock),spread=Math.max(.001,Math.abs(shock)*.8+vol*.2);bars.push({time:start+i*300000,open,high:Math.max(open,p)*(1+spread),low:Math.min(open,p)*(1-spread),close:p,volume:10000+(x%60000)})}return bars;
}
export function runReplay(symbol:string,cursor=240,strategy:StrategyName="Multi-Factor"){const session=ReplaySession.fromBars(seededBars(symbol),symbol),pipe=new QuantPipeline(strategy);const end=session.events[Math.min(cursor,session.events.length)-1]?.timestamp;session.replay(e=>pipe.onBar(e),undefined,end);return{session,snapshot:pipe.snapshot()};}
export function runBacktest(symbol:string,seed=17,strategy:StrategyName="Multi-Factor"){
 const session=ReplaySession.fromBars(seededBars(symbol,240,seed),symbol),pipe=new QuantPipeline(strategy); session.replay(e=>pipe.onBar(e)); const s=pipe.snapshot(); const returnPct=(s.equity-100000)/1000; return {symbol,strategy,events:s.eventsProcessed,equity:s.equity,realizedPnl:s.realizedPnl,unrealizedPnl:s.unrealizedPnl,drawdown:s.drawdown,exposure:s.exposure,fills:s.fills,returnPct};
}