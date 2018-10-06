from web3 import Web3, HTTPProvider
import json
import sqlite3
import os.path
import time

web3 = Web3(HTTPProvider('https://mainnet.infura.io/v3/d41025ea27ac416c8ec077e5ed8db4c8'))

# 6421267 is the latest block on 29-9-2018 14:32

# Create database and connect
db = 'new.db'
if not os.path.isfile(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''CREATE TABLE transactions
                 (block int, timestamp INT , trans_from text, trans_to text, hash text, gas text, gas_price text, value text, value_eth float)''')
    conn.commit()
else:
    conn = sqlite3.connect(db)
    c = conn.cursor()


# Get block and transaction data
for block_count in range(6326542, 6443000, 1):

    block = web3.eth.getBlock(block_count)
    timestamp_ = block["timestamp"]

    # Get maximum 10 transactions per block
    for tx_hash in block["transactions"][:10]:
        trans = web3.eth.getTransaction(tx_hash)
        tr_from = trans["from"]
        tr_to = trans["to"]
        gas = trans["gas"]
        gas_price = trans["gasPrice"]
        hash = trans["hash"]
        value = trans["value"]
        if int(value) == 0:
            continue
        value_eth = int(value) / 1000000000000000000

        c.execute("INSERT INTO transactions VALUES (?,?,?,?,?,?,?,?,?)", [block_count, timestamp_, tr_from, tr_to, hash.hex(), str(gas), str(gas_price), str(value), value_eth])
    print("Done with {}, amount of transaction: {}".format(block_count, len(block["transactions"])))
    conn.commit()
    time.sleep(1)

conn.close()
