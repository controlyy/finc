import utility.stock as stock
import json


# Opening portfolio file
f = open('portfolio.json')
data = json.load(f)
f.close()

# Update all stock date
for key, value in data['stock'].items():
    print("Updating " + key + ":" + value)
    stock.update_stock_to_db(key, 'db/stock.db')
