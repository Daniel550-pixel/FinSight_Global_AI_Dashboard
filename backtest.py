import pandas as pd
import matplotlib.pyplot as plt

def run_backtest(data):
    # voorbeeld simple moving average strategy
    data['SMA50'] = data['Close'].rolling(50).mean()
    data['Signal'] = 0
    data['Signal'][50:] = (data['Close'][50:] > data['SMA50'][50:]).astype(int)
    data['Returns'] = data['Close'].pct_change() * data['Signal'].shift(1)
    cumulative = (1 + data['Returns']).cumprod()
    cumulative.plot(title="Backtest cumulative returns")
    plt.savefig("backtest_plot.png")
    data.to_csv("backtest_results.csv")
