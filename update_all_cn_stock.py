import pandas as pd
import efinance as ef

# read list
stock_data = pd.read_excel('list/cn_stock_list.xlsx')

# add leading 0s
stock_data['Code'] = stock_data['Code'].apply('{:0>6}'.format)

# add new columns
stock_data['Sector'] = pd.NA
stock_data['PE'] = pd.NA
stock_data['PB'] = pd.NA
stock_data['ROE'] = pd.NA
stock_data['Market Cap'] = pd.NA
stock_data['Gross profit margin'] = pd.NA
stock_data['Profit margin'] = pd.NA

for i in range(len(stock_data)):
    print("Updating " + str(i))
    info = ef.stock.get_base_info(str(stock_data.loc[i, "Code"]))
    if info["股票代码"] != stock_data.loc[i, 'Code']:
        print("Error: code does not match. Original: " +
              str(stock_data.loc[i, 'Code']) + ". Retrieved:" + info["股票代码"])
    stock_data.loc[i, 'Sector'] = info["所处行业"]
    stock_data.loc[i, 'PE'] = info["市盈率(动)"]
    stock_data.loc[i, 'PB'] = info["市净率"]
    stock_data.loc[i, 'ROE'] = info["ROE"]
    stock_data.loc[i, 'Market Cap'] = info["总市值"]
    stock_data.loc[i, 'Gross profit margin'] = info["毛利率"]
    stock_data.loc[i, 'Profit margin'] = info["净利率"]
    

print(stock_data)
stock_data.to_excel('output.xlsx', sheet_name='s1', index=False)
