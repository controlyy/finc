import efinance as ef
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
        data = ef.stock.get_quote_history(
            ticker,
            beg=start_date.strftime("%Y%m%d"),
        )

        data = data.rename(
            columns={
                "日期": "date",
                "开盘": "open",
                "收盘": "close",
                "最高": "high",
                "最低": "low",
                "成交量": "volume"
            })

        data = data[['date', 'open', 'high', 'low', 'close', "volume"]]
        # print(data)
        data.to_sql(name=ticker, con=con, if_exists="append", index=False)

    # commit the changes to db
    con.commit()
    con.close()


def get_stock_1y_history(ticker):
    data = pd.DataFrame()
    try:
        start_date = datetime.datetime.today() - datetime.timedelta(days=381)
        data = ef.stock.get_quote_history(
            ticker,
            beg=start_date.strftime("%Y%m%d"),
        )

        data = data.rename(
            columns={
                "日期": "date",
                "开盘": "open",
                "收盘": "close",
                "最高": "high",
                "最低": "low",
                "成交量": "volume"
            })

        data = data[['date', 'open', 'high', 'low', 'close', "volume"]]
        data = data.set_index('date')
    except:
        print("Warning: cannot get data of '" + ticker + "'")

    return data


if __name__ == "__main__":
    update_stock_to_db('JPM', 'db/stock.db')
