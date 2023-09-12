"""Module to read stock data"""
import yfinance as yf
import sqlite3
import pandas as pd
import datetime


def update_stock_to_db(ticker, path_to_db):
    # connect db
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()

    # check if table exists
    cur.execute(
        "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" +
        ticker + "'")

    start_date = datetime.datetime(2005, 1, 1)

    if cur.fetchone()[0] == 1:
        print('Table exists: ' + ticker)
        cur.execute("SELECT date FROM " + ticker +
                    " ORDER BY date DESC LIMIT 1")
        latest_date_str = cur.fetchone()[0]
        start_date = datetime.datetime.strptime(latest_date_str, "%Y-%m-%d")
        start_date += datetime.timedelta(days=1)
    else:
        print('New table created: ' + ticker)

    if start_date >= (datetime.datetime.today() - datetime.timedelta(days=1)):
        print("Data is up to date")
    else:
        print("Get data after " + start_date.strftime("%Y-%m-%d"))
        data = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"))

        data['date'] = data.index
        data['date'] = data['date'].dt.strftime('%Y-%m-%d')

        data = data.rename(str.lower, axis='columns')
        data = data.rename(columns={"adj close": "adj_close"})
        data = data[[
            'date', 'open', 'high', 'low', 'close', "adj_close", "volume"
        ]]

        data.to_sql(name=ticker, con=con, if_exists="append", index=False)

    # commit the changes to db
    con.commit()
    con.close()


def convert_stock_number(ticker):
    if ticker.isnumeric():
        if ticker[0] == '6':
            ticker += '.ss'
        elif ticker[0] == '0':
            ticker += '.sz'
        elif ticker[0] == '3':
            ticker += '.sz'

    return ticker


def get_stock_history(ticker, period):
    ticker = convert_stock_number(ticker)

    data = yf.download(ticker, period=period)
    data = data.reset_index()
    data = data.rename(
        columns={
            "Date": "date",
            "Close": "close",
            "Open": "open",
            "High": "high",
            "Low": "low"
        })
    data = data.set_index('date')
    return data


def get_latest_price(ticker):
    df = yf.Ticker(ticker).history(interval="1m", period="1m")
    return df.iloc[-1]['Close']


def get_1week_price_change(ticker):
    ticker = convert_stock_number(ticker)
    df = yf.Ticker(ticker).history(period='1wk')
    start_price = df['Close'][0]
    end_price = df['Close'][-1]
    return (end_price - start_price) / start_price


def get_1month_price_change(ticker):
    ticker = convert_stock_number(ticker)
    df = yf.Ticker(ticker).history(interval='1wk', period='1mo')
    start_price = df['Close'][0]
    end_price = df['Close'][-1]
    return (end_price - start_price) / start_price


def get_1year_price_change(ticker):
    ticker = convert_stock_number(ticker)
    df = yf.Ticker(ticker).history(interval='1mo', period='1y')
    start_price = df['Close'][0]
    end_price = df['Close'][-1]
    return (end_price - start_price) / start_price


if __name__ == "__main__":
    # update_stock_to_db('JPM', 'db/stock.db')
    data = get_stock_history('600036', '1y')
    print(data)
