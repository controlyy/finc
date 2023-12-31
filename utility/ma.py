import pandas as pd


def get_dates_ma5_cross_ma60(original_data):
    data = pd.DataFrame()
    data['close'] = original_data['close']
    data['ma_5'] = data['close'].rolling(5).mean()
    data['ma_60'] = data['close'].rolling(60).mean()
    data = data.dropna()

    if data.iloc[-1]['ma_5'] > data.iloc[-1]['ma_60']:
        # already crossed
        days = 0
        for i in range(1, len(data)):
            if data.iloc[-i]['ma_5'] < data.iloc[-i]['ma_60']:
                break
            else:
                days -= 1
        return days

    rate_ma5 = data.iloc[-1]['ma_5'] - data.iloc[-2]['ma_5']
    rate_ma60 = data.iloc[-1]['ma_60'] - data.iloc[-2]['ma_60']

    if rate_ma5 < rate_ma60:
        return pd.NA

    days = (data.iloc[-1]['ma_60'] - data.iloc[-1]['ma_5']) / (rate_ma5 -
                                                               rate_ma60)
    return days


def if_all_ma_decline(data):
    data['ma_30'] = data['close'].rolling(30).mean()
    data['ma_60'] = data['close'].rolling(60).mean()
    data['ma_120'] = data['close'].rolling(120).mean()

    # if decline in last 10 days
    if (data.iloc[-1]['ma_30'] < data.iloc[-10]['ma_30']) and (
            data.iloc[-1]['ma_60'] < data.iloc[-10]['ma_60']) and (
                data.iloc[-1]['ma_120'] < data.iloc[-10]['ma_120']):
        return True

    return False
