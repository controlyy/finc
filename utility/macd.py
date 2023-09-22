import pandas as pd


def calculate_macd(data, fast=12, slow=26, ma=9):
    macd = pd.DataFrame()
    macd['close'] = data['close']
    macd = macd.reset_index()

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


def get_golden_cross_date(data):
    macd = calculate_macd(data)
    pos = macd['histogram'] >= 0
    neg = macd['histogram'] < 0
    golden_cross = data[pos & neg.shift(1)].index
    return golden_cross


def get_predicted_1_day_golden_cross_date(data):
    macd = calculate_macd(data)
    macd = macd.reset_index()
    date = pd.DataFrame()
    for i in range(1, len(macd)):
        if macd.loc[i, 'histogram'] < 0:
            rate = macd.loc[i, 'histogram'] - macd.loc[i - 1, 'histogram']
            if (macd.loc[i, 'histogram'] + rate) > 0:
                date = date.append(macd.iloc[i])

    date = date.set_index('date')
    return date.index


def get_death_cross_date(data):
    macd = calculate_macd(data)
    pos = macd['histogram'] >= 0
    neg = macd['histogram'] < 0
    death_cross = data[~(pos | neg.shift(1))].index
    return death_cross


def days_to_golden_cross(data):
    macd = calculate_macd(data)

    if macd.iloc[-1]['histogram'] > 0:
        # already pass the golden cross
        days = 0
        for i in range(1, len(macd)):
            if macd.iloc[-i]['histogram'] < 0:
                break
            else:
                days -= 1
        return days

    rate = macd.iloc[-1]['histogram'] - macd.iloc[-2]['histogram']

    if rate < 0:
        return pd.NA

    days = -macd.iloc[-1]['histogram'] / rate
    return days


def get_latest_macd(data):
    macd = calculate_macd(data)
    return macd.iloc[-1]['macd']
