import json
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import sys
import os
from web3.middleware import geth_poa_middleware
Cpath = os.path.dirname(os.path.realpath(__file__))

host = 'localhost'

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':3000'))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)
f = open(Cpath+'/users.json','r')
line = f.readline()
Jline = json.loads(line)
f.close()

abi = Jline['abi']
contract_address = Jline['contract_address']

# Contract instance in concise mode
contract_instance = w3.eth.contract(abi=abi, address=contract_address)

try:
    Email = w3.toBytes(text=sys.argv[1])
    result = contract_instance.functions.GetInfo(Email).call()
    nounce = w3.eth.getTransactionCount(w3.toChecksumAddress(result[0]))
    result.append(str(nounce))
    print(json.dumps(result))
except Exception as e:
    print(e)
    print("NULL")
