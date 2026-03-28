import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from scipy.stats import t as ft
from yahooquery import Ticker
import pandas as pd


def get_data(stocks, start, end):
    t = Ticker(stocks)

    hist = t.history(
        start=start.strftime('%Y-%m-%d'),
        end=end.strftime('%Y-%m-%d')
    )

    stockData = hist['close'].unstack(level=0)

    returns = stockData.pct_change().dropna()

    meanReturns = returns.mean()
    covMatrix = returns.cov()

    return meanReturns, covMatrix


stockList = ['NKE','PYPL','LULU']

endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(days=50)

meanReturns, covMatrix = get_data(stockList, startDate, endDate)

print(meanReturns)
print(covMatrix)

n = 3
weights = np.array([0.33,0.33,0.33])
total = weights.sum()
weights = weights / total

print("Portfolio weights", weights)
print("Sum of weights:", weights.sum())

mc_sims = 5000
T = 1000
df = 5

meanM = []
for day in range(T):
    meanM.append(meanReturns)

meanM = np.array(meanM)

L = np.linalg.cholesky(covMatrix)

portfolio_sims = []
initialPortfolio = 520

for m in range(mc_sims):
    Z = ft.rvs(df=df, size=(T, len(weights)))
    Z = Z / np.sqrt(df / (df - 2))

    dailyReturns = meanM + np.dot(Z, L.T)
    portfolio_dailyReturns = np.dot(dailyReturns, weights)

    portfolio_path = initialPortfolio * np.cumprod(1 + portfolio_dailyReturns)
    portfolio_path = np.insert(portfolio_path, 0, initialPortfolio)
    portfolio_path = np.maximum(portfolio_path, 0)

    portfolio_sims.append(portfolio_path)

plt.figure(figsize=(10, 8))
plt.plot(np.array(portfolio_sims).T)
plt.ylabel('Portfolio Value')
plt.xlabel('Days')
plt.show()


def max_drawdown(path):
    drawdown = (path - initialPortfolio) / initialPortfolio
    return drawdown.min()


portfolio_sims = np.array(portfolio_sims)

drawdowns = np.array([max_drawdown(path) for path in portfolio_sims])
print("\n" + "-"*40)
print("DRAWDOWN STATISTICS")
print(f'worst drawdown: {drawdowns.min():.3%}')
print(f"5% worst-case   drawdown: {np.percentile(drawdowns, 5):.2%}")
print(f"Median drawdown: {np.percentile(drawdowns, 50):.2%}")
print("\n" + "-"*40)
final_values = portfolio_sims[:, -1]

print("FINAL PORTFOLIO STATS")
print("\n" + "-"*40)
print(f"5% worst final value: ${np.percentile(final_values, 5):.0f}")
print(f"Median final value: ${np.percentile(final_values, 50):.0f}")
print(f"5% best final value: ${np.percentile(final_values, 95):.0f}")
average_finalvalue = np.mean(final_values)
print(f"AVERAGE FINAL VALUE: ${average_finalvalue:.0f}")
