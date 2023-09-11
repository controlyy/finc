import pandas as pd


def calculate_rsi(data, period=14):
    rsi = pd.DataFrame()
    rsi['close'] = data['Close']
    rsi = rsi.reset_index()
    rsi = rsi.rename(columns={"Date": "date"})

    if len(rsi.index) <= period:
        print("Error: Data size too small")
        return

    rsi['close_shift'] = rsi['close'].shift(1)
    rsi['gain'] = rsi['close'] - rsi['close_shift']
    rsi['loss'] = rsi['close_shift'] - rsi['close']
    rsi['gain'] = rsi['gain'].clip(lower=0)
    rsi['loss'] = rsi['loss'].clip(lower=0)

    rsi.loc[period, 'avg_gain'] = rsi['gain'].iloc[1:period + 1].mean()
    rsi.loc[period, 'avg_loss'] = rsi['loss'].iloc[1:period + 1].mean()

    for i in range(period + 1, len(rsi)):
        rsi.loc[i, 'avg_gain'] = (rsi.loc[i - 1, 'avg_gain'] *
                                  (period - 1) + rsi.loc[i, 'gain']) / period
        rsi.loc[i, 'avg_loss'] = (rsi.loc[i - 1, 'avg_loss'] *
                                  (period - 1) + rsi.loc[i, 'loss']) / period

    rsi['rs'] = rsi['avg_gain'] / rsi['avg_loss']
    rsi['rsi'] = 100 - (100 / (1 + rsi['rs']))

    rsi = rsi.set_index('date')
    rsi = rsi.drop(columns=[
        'close', 'close_shift', 'gain', 'loss', 'avg_gain', 'avg_loss', 'rs'
    ])
    rsi = rsi.dropna()

    return rsi
