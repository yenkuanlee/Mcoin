from web3 import Web3, HTTPProvider
import json
import sys

Rhash = sys.argv[1]
Tlist = list()

w3 = Web3(HTTPProvider('http://localhost:3000'))

tmp = Rhash.split(",")
for x in tmp:
    T = w3.eth.sendRawTransaction(x)
    Tlist.append(T)
print(json.dumps(T))
