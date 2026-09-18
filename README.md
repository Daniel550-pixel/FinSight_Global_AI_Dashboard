# FinSight Global AI Dashboard

A deterministic, browser-based quantitative trading terminal for market analysis, strategy simulation, backtesting, execution simulation, portfolio/P&L tracking, risk controls, and event-ledger observability.

## Current Integrations

- Order Book
- Replay Engine
- Execution Simulator
- Quant Pipeline
- Market Analysis
- L2 Market Depth
- Risk Gate
- Event Ledger
- Portfolio & P&L
- Deterministic Simulation
- Backtest Engine
- Strategy Registry
- Strategy UI
- Strategy-to-Pipeline
- Backtesting UI
- Strategy Comparison

## Web Terminal

The terminal provides modules for:

- Command Center
- Markets
- Replay Lab
- Order Book
- Strategies
- Backtesting
- Execution
- Risk
- Intelligence
- Alerts

## Local Development

Requirements:

- Node.js
- npm

```powershell
cd "$HOME\Downloads\FinSight_Global_AI_Dashboard\web"
npm install
npm run dev
```

Development server:

`http://localhost:8504`

## Architecture

```
Market Data
    ↓
Indicators / Market Analysis
    ↓
Strategy Registry
    ↓
Quant Pipeline
    ↓
Risk Gate
    ↓
Execution Simulator
    ↓
Portfolio / P&L
    ↓
Event Ledger
```

Replay and backtesting use deterministic seeded market data so simulations can be reproduced consistently.

## Project Structure

```
web/
├── app/
│   ├── page.tsx
│   ├── layout.tsx
│   └── globals.css
├── lib/
│   ├── market/
│   ├── replay/
│   ├── execution/
│   ├── quant/
│   ├── strategy/
│   ├── risk/
│   ├── ledger/
│   └── simulator.ts
├── next.config.ts
├── package.json
└── tsconfig.json
```

## Scope

FinSight is a research and simulation environment. Execution components currently operate as simulated/paper infrastructure rather than live brokerage execution.

## License

Private project.
