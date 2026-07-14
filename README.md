Web3 Arbitrage Platform
Project Overview

一个基于 Python + Docker 构建的 Web3 套利研究平台。
当前项目为了演示量化研究流程，Collector 每分钟拉取一次最新的 1 小时 K 线，用于持续更新 Analytics 指标；实际高频套利系统通常会采用 WebSocket 实时行情或 Tick 数据，而不是依赖小时级 K 线。

主要用于：

DEX/CEX Price Collection
Spread Monitoring
Quantitative Indicator Calculation
Strategy Backtesting
Dashboard Visualization

Tech Stack
Python
Docker Compose
MySQL
Dash
Pandas
Plotly
CCXT
Uniswap

Features
CEX Price Collection
DEX Price Collection

Spread Calculation
Moving Average
Rolling Standard Deviation
Z-score

Strategy Framework
 Mean Reversion
 Bollinger
 Momentum

Backtest Engine

Performance Metrics
Win Rate
Sharpe Ratio
Max Drawdown
Profit Factor
Average Holding Time

Interactive Dashboard

Future Work
Parameter Optimization
Multi-symbol Backtesting
Portfolio Management
Machine Learning Models
AI-assisted Strategy Research