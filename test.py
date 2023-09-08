import utility.stock
import utility.macd

data = utility.stock.get_stock_history('600036', '1y')
data_macd = utility.macd.calculate_macd(data)

data_macd.to_csv("test.csv")

