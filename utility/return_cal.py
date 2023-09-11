import pandas as pd


def calculate_return_rate(data, in_date, out_date):
    sr1 = pd.Series(1, index=in_date)
    sr2 = pd.Series(0, index=out_date)

    sr = sr1.append(sr2).sort_index()

    original_money = 10000
    money = original_money
    hold = 0
    last_trade_sell = True
    trade_times = 0

    for i in range(0, len(sr)):
        price = data['close'][sr.index[i]]
        if (sr.iloc[i] == 1) and (last_trade_sell):
            # golden cross
            hold = money // price
            money -= hold * price
            last_trade_sell= False
            trade_times += 1
        elif (sr.iloc[i] == 0) and (not last_trade_sell):
            # death cross
            money += hold * price
            hold = 0
            last_trade_sell= True

    price = data['close'][-1]
    total_money = hold * price + money - trade_times*5

    return_rate = (total_money - original_money) / original_money

    return return_rate
