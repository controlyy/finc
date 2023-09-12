import utility.stock as stock
import utility.stock_efinc as stock_efinc
import json


# Opening stock list file
f = open('snp500_stock.json')
data = json.load(f)
f.close()

# Update all stock date
for key, value in data.items():
    # class
    for sub_key, sub_value in data[key].items():
        print("Updating " + sub_key + ':' + sub_value)
        # stock.update_stock_to_db(sub_key, 'db/stock.db')
        stock_efinc.update_stock_to_db(sub_key, 'db/stock.db')
