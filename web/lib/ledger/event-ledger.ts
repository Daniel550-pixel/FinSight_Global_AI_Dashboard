export type LedgerEventType="market"|"strategy"|"risk"|"order"|"fill"|"portfolio";
export type LedgerEvent={sequence:number;timestamp:number;type:LedgerEventType;symbol:string;payload:Record<string,unknown>};
export class EventLedger{
 private readonly entries:LedgerEvent[]=[];
 append(timestamp:number,type:LedgerEventType,symbol:string,payload:Record<string,unknown>){const event={sequence:this.entries.length+1,timestamp,type,symbol,payload:{...payload}};this.entries.push(Object.freeze(event));return event;}
 get events(){return this.entries.slice();} latest(limit=25){return this.entries.slice(-limit).reverse();} count(type?:LedgerEventType){return type?this.entries.filter(e=>e.type===type).length:this.entries.length;}
}
