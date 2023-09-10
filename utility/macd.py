import pandas as pd


def calculate_macd(data, fast=12, slow=26, ma=9):
    macd = pd.DataFrame()
    macd['close'] = data['Close']
    macd = macd.reset_index()
    macd = macd.rename(columns={"Date": "date"})

    if (slow <= fast):
        print("Error: Slow smaller than Fast")
        return

    if len(macd.index) <= slow:
        print("Error: Data size too small")
        return

    macd.loc[0, 'fast_ma'] = macd.loc[0, 'close']
    macd.loc[0, 'slow_ma'] = macd.loc[0, 'close']

    macd['fast_ma'] = macd['close'].ewm(alpha=2 / (fast + 1),
                                        adjust=False).mean()
    macd['slow_ma'] = macd['close'].ewm(alpha=2 / (slow + 1),
                                        adjust=False).mean()
    macd['macd'] = macd['fast_ma'] - macd['slow_ma']
    macd['signal'] = macd['macd'].ewm(alpha=2 / (ma + 1), adjust=False).mean()
    macd['histogram'] = macd['macd'] - macd['signal']

    macd = macd.set_index('date')
    macd = macd.drop(columns=['close', 'slow_ma', 'fast_ma'])

    return macd
