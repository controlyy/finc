# encoding:utf-8

import pandas as pd
import utility.stock
import utility.macd
import utility.rsi
from tqdm.auto import tqdm

# read list
stock_data = pd.read_excel('list/cn_stock_list.xlsx')

# add leading 0s
stock_data['code'] = stock_data['code'].apply('{:0>6}'.format)
stock_data['macd_days'] = pd.NA
stock_data['macd'] = pd.NA
stock_data['rsi'] = pd.NA
stock_data['notice'] = pd.NA

#for i in tqdm(range(len(stock_data))):
for i in tqdm(range(10)):
    #print("Updating " + str(i))
    data = utility.stock.get_stock_history(str(stock_data.loc[i, "code"]),
                                           '2mo')

    if (len(data) < 20):
        print("Cannot get data of " + str(i))
        continue

    stock_data.loc[i, 'macd'] = utility.macd.get_latest_macd(data)
    stock_data.loc[i, 'macd_days'] = utility.macd.days_to_golden_cross(data)
    stock_data.loc[i, 'rsi'] = utility.rsi.get_current_rsi(data)

    if (stock_data.loc[i, 'macd_days'] is not pd.NA
        ) and (0 <= stock_data.loc[i, 'macd_days'] <= 3) and (
            stock_data.loc[i, 'macd'] < 0) and (stock_data.loc[i, 'rsi'] < 40):
        stock_data.loc[i, 'notice'] = '*'

stock_data = stock_data.set_index('code')
#print(stock_data)
stock_data.to_excel('test1.xlsx')