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
        "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='" + ticker + "'")

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

    if (start_date >= (datetime.datetime.today()-datetime.timedelta(days=1))):
        print("Data is up to date")
    else:
        print("Get data after " + start_date.strftime("%Y-%m-%d"))
        data = yf.download(ticker, start=start_date.strftime("%Y-%m-%d"))

        data['date'] = data.index
        data['date'] = data['date'].dt.strftime('%Y-%m-%d')

        data = data.rename(str.lower, axis='columns')
        data = data.rename(columns={"adj close": "adj_close"})
        data = data[['date', 'open', 'high',
                    'low', 'close', "adj_close", "volume"]]

        data.to_sql(name=ticker, con=con, if_exists="append", index=False)

    # commit the changes to db
    con.commit()
    con.close()


if __name__ == "__main__":
    update_stock_to_db('JPM', 'db/stock.db')
