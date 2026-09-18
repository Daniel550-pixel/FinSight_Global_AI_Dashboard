import {StrategyName} from "../strategy/registry";
import {runBacktest} from "../simulator";
import {EndToEndWorkflow} from "../quant/workflow";

export type TerminalState={
 symbol:string;
 strategy:StrategyName;
 engine:any;
 analysis:any;
 snapshot:any;
 backtest:ReturnType<typeof runBacktest>|null;
 comparison:ReturnType<typeof runBacktest>[]|null;
 alerts:any[];
 workflow:EndToEndWorkflow|null;
};

export function createTerminalState(symbol:string,strategy:StrategyName,engine:any,backtest:ReturnType<typeof runBacktest>|null=null,comparison:ReturnType<typeof runBacktest>[]|null=null,alerts:any[]=[],workflow:EndToEndWorkflow|null=null):TerminalState{
 return {symbol,strategy,engine,analysis:engine.snapshot.analysis,snapshot:engine.snapshot,backtest,comparison,alerts,workflow};
}
