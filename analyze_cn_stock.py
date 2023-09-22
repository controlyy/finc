# encoding:utf-8

import pandas as pd
import utility.stock
import utility.macd
import utility.rsi
import utility.ma
import utility.stock_efinc
from tqdm.auto import tqdm
import efinance as ef
from datetime import datetime

# read list
stock_data = pd.read_excel('list/cn_stock_list.xlsx', sheet_name='list')
stock_data = stock_data[['code', 'name', 'sector', 'note']]

# add leading 0s
stock_data['code'] = stock_data['code'].apply('{:0>6}'.format)
stock_data['sign'] = pd.NA
stock_data['gc_days'] = pd.NA
stock_data['ma5_cross_ma60_days'] = pd.NA
stock_data['macd'] = pd.NA
stock_data['rsi'] = pd.NA
stock_data['price'] = pd.NA
stock_data['1day%'] = pd.NA
stock_data['1week%'] = pd.NA
stock_data['1month%'] = pd.NA
stock_data['1year%'] = pd.NA
stock_data['pe ratio'] = pd.NA
stock_data['pb ratio'] = pd.NA
stock_data['roe'] = pd.NA
stock_data['gross profit margin'] = pd.NA
stock_data['net profit margin'] = pd.NA

for i in tqdm(range(len(stock_data))):
    #for i in tqdm(range(5)):
    #print("Updating " + str(i))
    ticker = str(stock_data.loc[i, "code"])
    data = utility.stock_efinc.get_stock_1y_history(ticker)

    if (len(data) < 60):
        print("Cannot get data of " + str(i))
        continue

    stock_data.loc[i, 'macd'] = round(utility.macd.get_latest_macd(data), 2)

    # check macd
    gc_days = utility.macd.days_to_golden_cross(data)
    if gc_days is not pd.NA:
        stock_data.loc[i, 'gc_days'] = round(gc_days, 2)

    # check rsi
    stock_data.loc[i, 'rsi'] = round(utility.rsi.get_current_rsi(data), 2)

    # check price and increase
    current_price = data['close'][-1]
    stock_data.loc[i, 'price'] = current_price

    yesterday_price = data['close'][-2]
    stock_data.loc[i, '1day%'] = round(
        (current_price - yesterday_price) / yesterday_price * 100, 2)

    one_week_price = data['close'][-5]
    stock_data.loc[i, '1week%'] = round(
        (current_price - one_week_price) / one_week_price * 100, 2)

    one_month_price = data['close'][-21]
    stock_data.loc[i, '1month%'] = round(
        (current_price - one_month_price) / one_month_price * 100, 2)

    one_year_price = data['close'][-240]
    stock_data.loc[i, '1year%'] = round(
        (current_price - one_year_price) / one_year_price * 100, 2)

    # check moving average
    dates_ma5_cross_ma60 = utility.ma.get_dates_ma5_cross_ma60(data)
    stock_data.loc[i, 'ma5_cross_ma60_days'] = dates_ma5_cross_ma60

    # check the signs
    if utility.ma.if_all_ma_decline(data):
        stock_data.loc[i, 'sign'] = ''
    else:
        stock_sign = ''

        if (dates_ma5_cross_ma60 is not pd.NA) and (-1 <= dates_ma5_cross_ma60
                                                    <= 3):
            stock_sign += '*'

        if (stock_data.loc[i, 'gc_days'] is
                not pd.NA) and (-1 <= stock_data.loc[i, 'gc_days'] <= 3):
            stock_sign += '*'

        # ignore if only rsi
        if (stock_sign != ''):
            if (stock_data.loc[i, 'macd'] < 0) and (stock_data.loc[i, 'rsi'] <
                                                    40):
                stock_sign += '*'

        stock_data.loc[i, 'sign'] = stock_sign

    # check base info
    base_info = ef.stock.get_base_info(ticker)
    stock_data.loc[i, 'pe ratio'] = base_info['市盈率(动)']
    stock_data.loc[i, 'pb ratio'] = base_info['市净率']
    stock_data.loc[i, 'roe'] = base_info['ROE']
    stock_data.loc[i, 'gross profit margin'] = round(base_info['毛利率'], 2)
    stock_data.loc[i, 'net profit margin'] = round(base_info['净利率'], 2)

stock_data = stock_data.set_index('code')

dt_string = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
stock_data.to_excel('output/cn_stock_analysis_' + dt_string + '.xlsx')
