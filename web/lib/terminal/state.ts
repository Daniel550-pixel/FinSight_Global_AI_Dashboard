import {StrategyName} from "../strategy/registry";
import {runBacktest} from "../simulator";

export type TerminalState={
 symbol:string;
 strategy:StrategyName;
 engine:any;
 analysis:any;
 snapshot:any;
 backtest:ReturnType<typeof runBacktest>|null;
 comparison:ReturnType<typeof runBacktest>[]|null;
 alerts:any[];
};

export function createTerminalState(symbol:string,strategy:StrategyName,engine:any,backtest:ReturnType<typeof runBacktest>|null=null,comparison:ReturnType<typeof runBacktest>[]|null=null,alerts:any[]=[]):TerminalState{
 return {symbol,strategy,engine,analysis:engine.snapshot.analysis,snapshot:engine.snapshot,backtest,comparison,alerts};
}
