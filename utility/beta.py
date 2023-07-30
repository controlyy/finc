
import pandas as pd
import logging
from scipy import stats
import sqlite3
import numpy as np


def calc_beta_to_spx(ticker):
    # read stock data
    conn = sqlite3.connect("db/stock.db")
    stock_data = pd.read_sql_query(
        "SELECT * FROM " + ticker + " ORDER BY date DESC LIMIT 251", conn)
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
            "stock data size and SPX size does not equal. stock size: " + str(len(stock_data)) + "; SPX size: " + str(len(spx_data)))
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


if __name__ == "__main__":
    stock = "JPM"
    beta = calc_beta_to_spx(stock)
    print("Stock '" + stock + "' beta is: " + str(beta))
