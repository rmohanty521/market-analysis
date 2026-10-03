import numpy as np
import pandas as pd


def daily_returns(prices):
    return prices.pct_change()


def rolling_vol(returns, window: int = 10):
    return returns.rolling(window).std() * np.sqrt(252)


def ann_vol(returns):
    return returns.std() * np.sqrt(252)


def sharpe(returns):
    return returns.mean() / returns.std() * np.sqrt(252)


def max_drawdown(prices):
    """Calculates a ratio of the price its on vs the highest price
    its seen up to that point. Then we subtract 1 from the ratio so
    it reflects how far away we are from that max. For example, 0.75
    turns into -0.25 meaning we are -0.25% from the max. Then we do
    .min to find the worst spot we were in relative to running peak
    at that point in time.

    """
    return (prices / prices.cummax() - 1).min()


def max_drawup(prices):
    return (prices / prices.cummin() - 1).max()


def stats(r):
    r = r.dropna()
    n = r.count()
    eq = (1 + r).cumprod()

    return {
        "Total ret": eq.iloc[-1] - 1,
        "Ann. ret": eq.iloc[-1] ** (252 / n) - 1,
        "Ann. Vol": ann_vol(r),
        "Sharpe": sharpe(r),
        "MaxDD": max_drawdown(eq),
    }


def inverse_vol_weights(r, window:int=20):
    '''returns weights in a 20 day window by default'''
    vol = rolling_vol(r, window=window) 
    inv_vol = 1/vol
    weights = inv_vol.div(inv_vol.sum(axis=1), axis=0)
    weights = weights.shift(1).dropna()

    return weights

def backtest_weights(weights, r, cost=0.005):
    pass


