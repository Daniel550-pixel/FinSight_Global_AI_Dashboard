import {seededBars} from "../simulator";
import {QuantPipeline} from "./pipeline";
import {StrategyName} from "../strategy/registry";
import {generateIntelligenceResponse,IntelligenceResult} from "../intelligence/engine";
import {generateAlerts,Alert} from "../alerts/engine";

export type WorkflowStageStatus="READY"|"ACTIVE"|"PASS"|"BLOCKED";
export type WorkflowStage={name:string;status:WorkflowStageStatus;detail:string;events:number};

export type EndToEndWorkflow={
  symbol:string;
  strategy:StrategyName;
  barsProcessed:number;
  stages:WorkflowStage[];
  snapshot:ReturnType<QuantPipeline["snapshot"]>;
  intelligence:IntelligenceResult;
  alerts:Alert[];
};

export function runQuantWorkflow(symbol:string,strategy:StrategyName="Multi-Factor",bars=240,seed=17):EndToEndWorkflow{
  const pipeline=new QuantPipeline(strategy);
  const input=seededBars(symbol,bars,seed);
  for(const bar of input) pipeline.onBar({symbol,timestamp:bar.time,price:bar.close,payload:bar});
  const snapshot=pipeline.snapshot();
  const ledger=snapshot.ledger??[];
  const has=(type:string)=>ledger.some((e:any)=>e.type===type);
  const stages:WorkflowStage[]=[
    {name:"MARKET",status:snapshot.eventsProcessed>0?"PASS":"READY",detail:`${snapshot.eventsProcessed} bars ingested`,events:snapshot.eventsProcessed},
    {name:"ANALYSIS",status:snapshot.analysis?"PASS":"READY",detail:snapshot.analysis?`${snapshot.analysis.regime} / score ${snapshot.analysis.score}`:"Waiting for analysis window",events:has("market")?1:0},
    {name:"STRATEGY",status:has("strategy")?"PASS":"READY",detail:snapshot.strategy,events:ledger.filter((e:any)=>e.type==="strategy").length},
    {name:"RISK GATE",status:snapshot.riskDecision?(snapshot.riskDecision.allowed?"PASS":"BLOCKED"):"READY",detail:snapshot.riskDecision?(snapshot.riskDecision.allowed?"Signal permitted":"Signal blocked"):"No decision",events:ledger.filter((e:any)=>e.type==="risk").length},
    {name:"ORDER",status:has("order")?"PASS":"READY",detail:has("order")?"Order submitted":"No order submitted",events:ledger.filter((e:any)=>e.type==="order").length},
    {name:"EXECUTION",status:snapshot.fills>0?"PASS":snapshot.openOrders>0?"ACTIVE":"READY",detail:`${snapshot.fills} fills / ${snapshot.openOrders} open`,events:ledger.filter((e:any)=>e.type==="fill").length},
    {name:"PORTFOLIO",status:has("portfolio")?"PASS":"READY",detail:`Equity $${snapshot.equity.toFixed(2)}`,events:ledger.filter((e:any)=>e.type==="portfolio").length},
    {name:"EVENT LEDGER",status:ledger.length>0?"PASS":"READY",detail:`${ledger.length} recent events`,events:ledger.length},
    {name:"INTELLIGENCE",status:"PASS",detail:"Deterministic explanation ready",events:1},
    {name:"ALERTS",status:"PASS",detail:"Rule engine evaluated",events:0}
  ];
  const intelligence=generateIntelligenceResponse("",{symbol,strategy,price:snapshot.lastPrice,analysis:snapshot.analysis,snapshot,backtest:null});
  const alerts=generateAlerts(snapshot,symbol);
  return {symbol,strategy,barsProcessed:input.length,stages,snapshot,intelligence,alerts};
}
