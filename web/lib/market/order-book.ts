export type Side="bid"|"ask";
export type Level={price:number;quantity:number};
export class OrderBook{
 bids=new Map<number,number>(); asks=new Map<number,number>(); sequence=0; timestamp=0;
 snapshot(bids:Level[],asks:Level[],timestamp=0,sequence?:number){this.bids=new Map(bids.filter(x=>x.quantity>0).map(x=>[x.price,x.quantity]));this.asks=new Map(asks.filter(x=>x.quantity>0).map(x=>[x.price,x.quantity]));this.advance(timestamp,sequence)}
 update(side:Side,price:number,quantity:number,timestamp=0,sequence?:number){const b=side==="bid"?this.bids:this.asks;if(quantity<=0)b.delete(price);else b.set(price,quantity);this.advance(timestamp,sequence)}
 bestBid(){const x=[...this.bids.entries()].sort((a,b)=>b[0]-a[0])[0];return x?{price:x[0],quantity:x[1]}:null}
 bestAsk(){const x=[...this.asks.entries()].sort((a,b)=>a[0]-b[0])[0];return x?{price:x[0],quantity:x[1]}:null}
 mid(){const b=this.bestBid(),a=this.bestAsk();return b&&a?(b.price+a.price)/2:null}
 spread(){const b=this.bestBid(),a=this.bestAsk();return b&&a?a.price-b.price:null}
 microprice(){const b=this.bestBid(),a=this.bestAsk();if(!b||!a)return null;const t=b.quantity+a.quantity;return t?(a.price*b.quantity+b.price*a.quantity)/t:null}
 depth(levels=10){return{bids:[...this.bids].sort((a,b)=>b[0]-a[0]).slice(0,levels).map(([price,quantity])=>({price,quantity})),asks:[...this.asks].sort((a,b)=>a[0]-b[0]).slice(0,levels).map(([price,quantity])=>({price,quantity}))}}
 imbalance(levels=5){const d=this.depth(levels),b=d.bids.reduce((s,x)=>s+x.quantity,0),a=d.asks.reduce((s,x)=>s+x.quantity,0);return b+a?(b-a)/(b+a):0}
 queueAhead(side:Side,price:number){return Math.max(0,(side==="bid"?this.bids:this.asks).get(price)||0)}
 private advance(timestamp:number,sequence?:number){this.timestamp=timestamp;this.sequence=sequence??this.sequence+1}
}