import utility.stock
import utility.macd
import utility.rsi

data = utility.stock.get_stock_history('AAPL', '1y')
#data_macd = utility.macd.calculate_macd(data)
#data_macd['close'] = data['Close']
#data_macd.to_csv("test.csv")

#data_rsi = utility.rsi.calculate_rsi(data)
#data_rsi.to_csv("test.csv")

data_macd = utility.macd.get_golden_cross_date(data)
print(data_macd)

