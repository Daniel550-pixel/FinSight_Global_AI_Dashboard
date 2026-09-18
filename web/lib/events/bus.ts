export type FinSightEvent={sequence:number;timestamp:number;type:string;symbol:string;source:string;payload:Record<string,any>};

export class EventBus{
 private sequence=0;
 private events:FinSightEvent[]=[];
 emit(type:string,symbol:string,source:string,payload:Record<string,any>={}){
  const event={sequence:++this.sequence,timestamp:Date.now(),type,symbol,source,payload};
  this.events.unshift(event);
  if(this.events.length>200)this.events.pop();
  return event;
 }
 latest(limit=50){return this.events.slice(0,limit);}
 clear(){this.events=[];this.sequence=0;}
}
