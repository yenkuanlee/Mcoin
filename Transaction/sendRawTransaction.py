from web3 import Web3, HTTPProvider
import sys
Rhash = sys.argv[1]

w3 = Web3(HTTPProvider('http://localhost:3000'))
T = w3.eth.sendRawTransaction(Rhash)
print(T)
