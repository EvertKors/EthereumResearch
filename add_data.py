import csv
import sqlite3
db = "new.db"

min = 1536639507 - 3000
max = 1536881115 + 3000
price_data = "https://www.cryptodatadownload.com/cdd/gemini_ETHUSD_2018_1min.csv"

conn = sqlite3.connect(db)
c = conn.cursor()
with open(price_data) as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    next(data)
    next(data)

    prevTimestamp = 9999999999
    for row in data:
        timestamp = int(row[0][:10])

        if not (min <= timestamp <= max ):
            continue

        c.execute('UPDATE main.transactions SET price_eth = {} WHERE timestamp < {} and timestamp >= {}'.format(
                row[4], prevTimestamp, timestamp
        ))
        conn.commit()
        print(timestamp)
        prevTimestamp = timestamp


