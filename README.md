# Fast ADX and EMA Indicator Library

This library provides a fast and efficient implementation of the Average Directional Movement Index (ADX) and Exponential Moving Average (EMA) for financial market data. It is designed to overcome performance issues in the widely-used `ta` library, which can lead to significant delays when importing functions, especially for real-time trading signals.

## Problem with the `ta` Library

The `ta` library is a great tool for technical analysis, but it has certain drawbacks:
- **Long import times**: Loading the entire library can cause delays, which is problematic when you need fast execution for real-time trading or backtesting.
- **Increased latency**: Due to the overhead of the library, indicators such as ADX and EMA may take longer to compute, leading to delayed signals and slower decision-making.

## Solution: Fast ADX and EMA Indicator

To solve this issue, we built a lightweight and fast alternative for calculating ADX and EMA indicators. This library ensures:
- **Minimal Import Time**: Only the required functionality is imported, reducing the initialization overhead.
- **Faster Execution**: The indicators are calculated in milliseconds, making this library ideal for real-time signal generation and backtesting.
- **Custom Implementation**: Currently, the library only includes the ADX and EMA indicators, making it more focused and optimized for these calculations.

## Features

- **Average Directional Movement Index (ADX)**: A momentum indicator used to determine the strength of a trend.
- **Exponential Moving Average (EMA)**: A type of moving average that gives more weight to recent prices, making it more responsive to new data.
- **Fast Execution**: Both indicators are computed within milliseconds to avoid delays in signal generation.

## Installation

Clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/fast-adx-ema-indicator.git
