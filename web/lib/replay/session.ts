export type MarketEvent={timestamp:number;eventType:string;symbol:string;side?:string;price?:number;quantity?:number;sequence?:number;payload?:Record<string,number|string>};
export class ReplaySession{
 static FORMAT="FINSIGHT-REPLAY-1";
 readonly events:MarketEvent[];
 constructor(events:MarketEvent[]=[]){this.events=[...events].sort((a,b)=>a.timestamp-b.timestamp||(a.sequence??0)-(b.sequence??0))}
 get start(){return this.events[0]?.timestamp??null} get end(){return this.events.at(-1)?.timestamp??null}
 replay(handler:(e:MarketEvent)=>void,start?:number,end?:number){let n=0;for(const e of this.events){if(start!==undefined&&e.timestamp<start)continue;if(end!==undefined&&e.timestamp>end)break;handler(e);n++}return n}
 static fromBars(bars:{time:number;open:number;high:number;low:number;close:number;volume:number}[],symbol:string){return new ReplaySession(bars.map((b,i)=>({timestamp:b.time,eventType:"bar",symbol,price:b.close,quantity:b.volume,sequence:i,payload:b})))} 
 toJSON(){return JSON.stringify({format:ReplaySession.FORMAT,event_count:this.events.length,events:this.events})}
}