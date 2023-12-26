import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np

# Define the list of tickers and the benchmark
tickers_reduced = [
    "FSLR", "ENPH", "SEDG", "SUZLON.NS", "SHLS", "CMIG4.SA", "ARRY", "ERG.MI", 
    "VER.VI", "NHPC.NS", "S92.DE", "300274.SZ", "ECV.DE", "6865.HK", "0586.HK", 
    "NEOEN.PA", "ENELAM.SN", "VBK.DE", "1798.HK", "000591.SZ", "601016.SS"
]
benchmark_ticker = "ICLN"

# Download historical data
start_date = datetime.today() - timedelta(days=5*365)
end_date = datetime.today()

data_reduced = yf.download(tickers_reduced, start=start_date, end=end_date)['Adj Close']
data_benchmark = yf.download(benchmark_ticker, start=start_date, end=end_date)['Adj Close']

# Calculate the average daily returns for each asset in the portfolio
returns_reduced = data_reduced.pct_change().dropna()
cumulative_returns_reduced = (1 + returns_reduced).cumprod()

# Calculate overall portfolio returns
returns_reduced_ov = data_reduced.pct_change().mean(axis=1)
cumulative_returns_reduced_ov = (1 + returns_reduced_ov).cumprod()

# Calculate the benchmark returns
returns_benchmark = data_benchmark.pct_change().dropna()
cumulative_returns_benchmark = (1 + returns_benchmark).cumprod()

# Calculate the volatility of each asset in the portfolio (std)
volatilities = returns_reduced.std()

# Calculate the correlation matrix between assets
correlation_matrix = returns_reduced.corr()

# Define the weights of the assets in the portfolio (equal-weight portfolio)
weights = np.array([1/len(tickers_reduced)] * len(tickers_reduced))

# Initialize portfolio volatility
portfolio_volatility = 0

# Double summation over the assets to calculate the portfolio volatility
for i in range(len(tickers_reduced)):
    for j in range(len(tickers_reduced)):
        portfolio_volatility += weights[i] * weights[j] * volatilities[i] * volatilities[j] * correlation_matrix.iloc[i, j]

portfolio_volatility = np.sqrt(portfolio_volatility) * np.sqrt(252)  # Annualize the volatility

# Calculate the average annual portfolio return
annual_returns_reduced_ov = (1 + returns_reduced_ov).resample('Y').prod() - 1
average_annual_return_reduced_ov = annual_returns_reduced_ov.mean()

# Assuming an annual risk-free rate of 0.0312
risk_free_rate_annual = 0.0312

# Calculate the Sharpe Ratio of the portfolio
sharpe_ratio_portfolio = (average_annual_return_reduced_ov - risk_free_rate_annual) / portfolio_volatility

# Calculate the volatility of the benchmark
volatility_benchmark = returns_benchmark.std() * np.sqrt(252)

# Calculate the annual return of the benchmark
annual_return_benchmark = (1 + returns_benchmark).resample('Y').prod() - 1
average_annual_return_benchmark = annual_return_benchmark.mean()

# Calculate the Sharpe Ratio of the benchmark
sharpe_ratio_benchmark = (average_annual_return_benchmark - risk_free_rate_annual) / volatility_benchmark

import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# Define the list of tickers and the benchmark
tickers_reduced = [
    # ... (same as before)
]
benchmark_ticker = "ICLN"

# Download historical data
# ... (same as before)

# Calculate metrics
# ... (same as before)

# Prepare annualized returns in a tabular format
annual_returns_reduced_ov_table = annual_returns_reduced_ov.reset_index()
annual_returns_reduced_ov_table.columns = ['Year', 'Portfolio Return']
annual_returns_reduced_ov_table['Year'] = annual_returns_reduced_ov_table['Year'].dt.year
annual_returns_reduced_ov_table['Average Return'] = annual_returns_reduced_ov_table['Portfolio Return'].mean()

annual_return_benchmark_table = annual_return_benchmark.reset_index()
annual_return_benchmark_table.columns = ['Year', 'Benchmark Return']
annual_return_benchmark_table['Year'] = annual_return_benchmark_table['Year'].dt.year
annual_return_benchmark_table['Average Return'] = annual_return_benchmark_table['Benchmark Return'].mean()


# Calculate drawdowns for the portfolio and benchmark
rolling_max_reduced = cumulative_returns_reduced_ov.cummax()
drawdowns_reduced = (cumulative_returns_reduced_ov - rolling_max_reduced) / rolling_max_reduced
max_drawdown_reduced = drawdowns_reduced.min()
rolling_max_benchmark = cumulative_returns_benchmark.cummax()
drawdowns_benchmark = (cumulative_returns_benchmark - rolling_max_benchmark) / rolling_max_benchmark
max_drawdown_benchmark = drawdowns_benchmark.min()

# Open a file to write the metrics
with open('../assets/portfolio_metrics_report.txt', 'w') as file:
    file.write("Portfolio Performance Report\n")
    file.write("===========================\n\n")

    file.write("Returns\n")
    file.write("-------\n")
    file.write(" - Cumulative Returns\n")
    file.write("       Portfolio: {:.2f}%\n".format((cumulative_returns_reduced_ov.iloc[-1] - 1) * 100))
    file.write("       Benchmark: {:.2f}%\n\n".format((cumulative_returns_benchmark.iloc[-1] - 1) * 100))

    file.write(" - Annualized Returns\n")
    file.write("      Portfolio\n")
    file.write(annual_returns_reduced_ov_table.to_string(index=False))
    file.write("\n\n      Benchmark\n")
    file.write(annual_return_benchmark_table.to_string(index=False))
    file.write("\n\n")

    file.write("Portfolio Analysis\n")
    file.write("------------------\n")
    file.write("Portfolio Sharpe Ratio: {:.2f}\n".format(sharpe_ratio_portfolio))
    file.write("Portfolio Volatility: {:.2f}\n".format(portfolio_volatility))
    file.write("Average Annual Portfolio Return: {:.2f}%\n".format(average_annual_return_reduced_ov * 100))
    file.write("\n\n")
    
    file.write("Benchmark Analysis\n")
    file.write("------------------\n")
    file.write("Benchmark Sharpe Ratio (ICLN): {:.2f}\n".format(sharpe_ratio_benchmark))
    file.write("Benchmark Volatility (ICLN): {:.2f}\n".format(volatility_benchmark))
    file.write("Average Annual Benchmark Return (ICLN): {:.2f}%\n".format(average_annual_return_benchmark * 100))
    file.write("\n\n")
     
    file.write("Maximum Drawdown Analysis\n")
    file.write("------------------------\n")
    file.write(f"Maximum Drawdown Portfolio: {max_drawdown_reduced * 100:.2f}%\n")
    file.write(f"Maximum Drawdown Benchmark: {max_drawdown_benchmark * 100:.2f}%\n")




# Comparison chart for cumulative returns
plt.figure(figsize=(12, 6))
plt.plot(cumulative_returns_reduced_ov, label='REAP', color='blue')
plt.plot(cumulative_returns_benchmark, label='ICLN', color='green')
plt.title('Cumulative Returns Comparison: REAP vs. ICLN ETF')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns (Multiplicative Factor)')
plt.legend()
plt.grid(True)
plt.savefig('../assets/cumulative_returns.png')

# Drawdown comparison chart
plt.figure(figsize=(12, 6))
drawdowns_reduced.plot(label='Reduced Portfolio', color='blue')
drawdowns_benchmark.plot(label='ICLN ETF', color='green')
plt.title('Drawdown Comparison')
plt.xlabel('Date')
plt.ylabel('Drawdown')
plt.legend()
plt.grid(True)
plt.savefig('../assets/drawdown.png')



