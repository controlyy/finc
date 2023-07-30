import pandas as pd
import os
from json import loads, dumps


def stock_list_to_json(excel_file, output_file_name):
    if not os.path.isfile(excel_file):
        print("File '" + excel_file + "' does not exist")
        return
    data = pd.read_excel(excel_file,)
    data = data.set_index('sector')
    print(data)
    result = data.to_json(orient='table')
    parsed = loads(result)
    print(dumps(parsed, indent=4))
    print("Data from '" + excel_file +
          "' is written to '" + output_file_name + "'")


if __name__ == "__main__":
    stock_list_to_json('S&P500 list.xlsx', "us_stock.json")
