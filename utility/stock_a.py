import efinance as ef
# 股票代码
stock_code = 'AAPL'
data = ef.stock.get_quote_history(stock_code)
print(data)
