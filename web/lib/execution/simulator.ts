export type Fill={orderId:number;timestamp:number;symbol:string;side:"buy"|"sell";price:number;quantity:number;fee:number};
type Order={id:number;symbol:string;side:"buy"|"sell";quantity:number;price?:number;remaining:number;type:"market"|"limit"};
export class ExecutionSimulator{
 feeBps:number;slippageBps:number;orders=new Map<number,Order>();fills:Fill[]=[];private next=1;
 constructor(feeBps=1,slippageBps=2){this.feeBps=feeBps;this.slippageBps=slippageBps}
 submit(symbol:string,side:"buy"|"sell",quantity:number,price?:number,type:"market"|"limit"="market"){if(quantity<=0)throw Error("quantity must be positive");if(type==="limit"&&!price)throw Error("limit price required");const id=this.next++;this.orders.set(id,{id,symbol,side,quantity,price,remaining:quantity,type});return id}
 processBar(symbol:string,timestamp:number,o:number,h:number,l:number,c:number){const out:Fill[]=[];for(const order of [...this.orders.values()]){if(order.symbol!==symbol)continue;let px:number|undefined=order.price;if(order.type==="market")px=o*(1+(order.side==="buy"?1:-1)*this.slippageBps/10000);else if(order.side==="buy"&&l<=(order.price??Infinity))px=order.price;else if(order.side==="sell"&&h>=(order.price??-Infinity))px=order.price;else continue;const fee=px! * order.remaining*this.feeBps/10000;const fill={orderId:order.id,timestamp,symbol,side:order.side,price:px!,quantity:order.remaining,fee};out.push(fill);this.fills.push(fill);this.orders.delete(order.id)}return out}
 cancel(id:number){return this.orders.delete(id)}
}