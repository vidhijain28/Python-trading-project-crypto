# Multi-Crypto Event-Driven Trading System

End-to-end multi-cryptocurrency trading research and backtesting framework using Binance public REST API data.

Multi-Crypto Event-Driven Trading & Backtesting Framework

# Overview

This project implements an end-to-end quantitative trading research framework for cryptocurrency markets. The system supports the complete research lifecycle—from historical market data acquisition and feature engineering to event-driven backtesting and forward testing using the Alpaca Paper Trading API.

Unlike a simple strategy notebook, the project is organized as a modular trading system with separate components for data ingestion, signal generation, order management, execution simulation, portfolio accounting, and forward deployment.

The framework was developed to emulate the architecture commonly used by systematic trading firms while remaining flexible enough to test new alpha signals and execution logic.

# Objectives

The primary objectives of the project are to:

Build a reusable quantitative research framework rather than a single trading strategy.
Implement an event-driven trading architecture capable of supporting multiple cryptocurrencies simultaneously.
Design and evaluate cross-sectional momentum signals using high-frequency market data.
Simulate realistic order execution through an order book and matching engine.
Measure portfolio performance under historical backtesting.
Validate research results through live forward testing using Alpaca Paper Trading.

# Project Architecture

                Binance Historical API
                         │
                         ▼
             Historical OHLCV Data
                         │
                         ▼
               Data Cleaning Pipeline
                         │
                         ▼
              Feature Engineering
                         │
                         ▼
           Strategy Signal Generation
                         │
                         ▼
                Order Management
                         │
                         ▼
                  Order Book
                         │
                         ▼
                Matching Engine
                         │
                         ▼
             Portfolio Accounting
                         │
                         ▼
          Performance Analytics
                         │
                         ▼
        Alpaca Paper Trading API
Trading Universe

The framework currently supports simultaneous trading across multiple cryptocurrencies.

# Default universe:

BTCUSDT
ETHUSDT
BNBUSDT
SOLUSDT
XRPUSDT

Additional assets can be added by modifying a single configuration file.

# Data Sources
Historical Research

Historical market data is downloaded directly from the Binance public REST API.

# Features:

5-minute OHLCV candles
Multi-year historical dataset
No authentication required
Automatic pagination
Automatic retry logic
Local parquet caching
Forward Testing

Forward testing is performed through Alpaca Paper Trading.

# The framework supports:

Live market data
Portfolio monitoring
Position tracking
Paper order submission
Trade logging
Performance monitoring

No real capital is used.

# Feature Engineering

The framework transforms raw market data into predictive features.

Implemented features include:

Return Features
5-minute returns
Log returns
Multi-horizon momentum
Trend Features
Short moving averages
Long moving averages
Moving average spread
Risk Features
Rolling volatility
Volatility ranking
Cross-sectional volatility
Cross-Sectional Features

Assets are ranked every timestamp using:

Momentum percentile
Volatility percentile
Composite signal ranking

These rankings determine which assets enter and exit the portfolio.

Strategy

The default implementation uses a cross-sectional momentum strategy.

# Workflow:

Compute momentum for every cryptocurrency.
Rank all assets simultaneously.
Buy strongest assets.
Exit weakest assets.
Size positions according to portfolio constraints.

The strategy class is modular and can easily be replaced with:

Mean reversion
Statistical arbitrage
Machine learning models
Reinforcement learning
Market making
Event-Driven Backtester

The backtester simulates a realistic trading environment.

Components include:

Gateway

Streams historical data bar-by-bar to emulate live market updates.

Strategy Engine

Generates trading signals from incoming market data.

Order Manager

Validates:

Available capital
Position limits
Exposure constraints
Order Book

Maintains:

Buy orders
Sell orders
Price-time priority
Matching Engine

Simulates:

Full fills
Partial fills
Order cancellations
Slippage
Transaction costs
Portfolio Engine

Tracks:

Cash
Positions
Equity
Unrealized P&L
Realized P&L
Performance Evaluation

# The framework computes portfolio-level metrics including:

Total Return
Annualized Return
Sharpe Ratio
Maximum Drawdown
Win Rate
Number of Trades
Equity Curve
Portfolio Value
Exposure Statistics

Additional metrics can be integrated easily.

Forward Testing with Alpaca

Following historical validation, the strategy can be deployed to Alpaca Paper Trading.

# The deployment notebook:

connects to Alpaca Paper Trading,
downloads recent crypto market data,
regenerates trading signals,
checks current positions,
submits paper orders,
records all executions,
logs signals and trades.

The project therefore supports both historical research and live paper validation.

# Technologies Used

## Programming

Python

## Data Processing

NumPy
pandas
PyArrow

## Machine Learning & Analytics

scikit-learn

## Market Data

Binance REST API
Alpaca Market Data API

## Execution

Alpaca Paper Trading API

## Development

Jupyter Notebook
