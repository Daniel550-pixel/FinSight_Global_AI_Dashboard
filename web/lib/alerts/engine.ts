export type AlertSeverity="HIGH"|"MED"|"LOW"|"INFO";
export type Alert={id:string;timestamp:number;severity:AlertSeverity;type:string;title:string;message:string;symbol:string};

export function generateAlerts(snapshot:any,symbol:string,previous?:any):Alert[]{
 const now=Date.now(),out:Alert[]=[];
 const push=(id:string,severity:AlertSeverity,type:string,title:string,message:string)=>out.push({id: id+"-"+now,timestamp:now,severity,type,title,message,symbol});
 const drawdown=Number(snapshot?.drawdown??0),imbalance=Number(snapshot?.imbalance??0),risk=snapshot?.riskDecision;
 if(drawdown>=5)push("drawdown","HIGH","RISK","Drawdown guard",`Portfolio drawdown reached ${drawdown.toFixed(2)}%, at or above the configured 5% threshold.`);
 else push("drawdown","INFO","RISK","Drawdown guard",`Portfolio drawdown remains at ${drawdown.toFixed(2)}%, below the 5% threshold.`);
 if(Math.abs(imbalance)>=0.18)push("imbalance","LOW","MICROSTRUCTURE","Order-book imbalance",`Simulated book imbalance is ${(imbalance*100).toFixed(1)}%.`);
 if(risk&&!risk.allowed)push("risk-gate","HIGH","RISK","Risk gate blocked",`Current signal was blocked: ${(risk.reasons??[]).join(" ")||"risk constraints active"}`);
 if(snapshot?.fills>0)push("execution","LOW","EXECUTION","Execution activity",`${snapshot.fills} fills recorded with ${snapshot.openOrders??0} open orders.`);
 const latest=snapshot?.ledger?.find((e:any)=>e.type==="strategy");
 if(latest)push("strategy","MED","STRATEGY","Strategy signal",`${latest.data?.strategy??"Strategy"} generated ${String(latest.data?.side??"hold").toUpperCase()} with score ${latest.data?.score??0}.`);
 if(previous?.analysis?.regime&&snapshot?.analysis?.regime&&previous.analysis.regime!==snapshot.analysis.regime)push("regime-change","MED","REGIME","Volatility regime changed",`Regime changed from ${previous.analysis.regime} to ${snapshot.analysis.regime}.`);
 return out;
}
