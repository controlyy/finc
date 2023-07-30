
import pandas as pd
import logging
from scipy import stats
import sqlite3
import numpy as np
import json
import matplotlib.pyplot as plt


def calc_beta_to_spx(ticker):
    # read stock data
    conn = sqlite3.connect("db/stock.db")
    stock_data = pd.read_sql_query(
        "SELECT * FROM '" + ticker + "' ORDER BY date DESC LIMIT 251", conn)
    # print(stock_data)
    conn.close()

    # read spx data
    conn = sqlite3.connect("db/index.db")
    spx_data = pd.read_sql_query(
        "SELECT * FROM 'SPX' ORDER BY date DESC LIMIT 251", conn)
    # print(spx_data)
    conn.close()

    if len(stock_data) != len(spx_data):
        logging.error(
            "stock data size and SPX size does not equal. " + ticker + " size: " + str(len(stock_data)) + "; SPX size: " + str(len(spx_data)))
        return 0

    spx_pct_change = spx_data['close'].pct_change()[1:]
    stock_pct_change = stock_data['close'].pct_change()[1:]

    # print(spx_pct_change)
    # print(stock_pct_change)

    # result = stats.linregress(spx_pct_change, stock_pct_change)
    # print(result)

    beta = (np.cov(stock_pct_change, spx_pct_change)
            [0][1]) / np.var(spx_pct_change)
    # print("The stock beta is " + str(beta))
    return beta


def get_all_stock_beta(stock_list):
    stock_beta = pd.DataFrame()

    stock_beta.insert(0, 'ticker', value='')
    stock_beta.insert(1, 'beta', value='')
    # print(stock_beta)

    for index, row in stock_list.iterrows():
        beta = calc_beta_to_spx(row['ticker'])
        new_row = pd.Series([row['ticker'], beta], index=['ticker', 'beta'])
        stock_beta = stock_beta._append(new_row, ignore_index=True)

    return stock_beta


if __name__ == "__main__":
    # stock = "JPM"
    # beta = calc_beta_to_spx(stock)
    # print("Stock '" + stock + "' beta is: " + str(beta))

    # Opening stock list file
    f = open('snp500_stock.json')
    stock_json = json.load(f)
    f.close()

    stock_list = pd.DataFrame()
    stock_list.insert(0, 'ticker', value='')
    # print(stock_list)

    # Update all stock date
    for key, value in stock_json.items():
        # class
        for sub_key, sub_value in stock_json[key].items():
            # print("Updating " + sub_key + ':' + sub_value)
            new_row = pd.Series([sub_key], index=['ticker'])
            stock_list = stock_list._append(new_row, ignore_index=True)

    stock_beta = get_all_stock_beta(stock_list)
    # print(stock_beta)

    stock_beta.insert(2, 'rret', value='')
    # print(stock_beta)

    risk_free_return = 0.05
    market_return = 0.135

    for index, row in stock_beta.iterrows():
        rret = risk_free_return + \
            (market_return-risk_free_return) * row['beta']
        stock_beta.at[index, 'rret'] = rret

    print(stock_beta)
    x = stock_beta['beta']
    y = stock_beta['rret']
    plt.plot(x,y,'bo')
    #print(x)
    plt.show()
