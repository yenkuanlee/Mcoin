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
SuperAccount = "0x42946c2bb22ad422e7366d68d3ca07fb1862ff36"

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':3000'))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)
SuperAccount = w3.toChecksumAddress(SuperAccount)
f = open(Cpath+'/abi','r')
line = f.readline()
Jline = json.loads(line)
f.close()

abi = Jline
contract_address = "0x06E8b961683Ed5CE732748bF6bcaFF2aAedb689E"

# Contract instance in concise mode
contract_instance = w3.eth.contract(abi=abi, address=contract_address)

address = w3.toChecksumAddress(sys.argv[1])
result = contract_instance.functions.balanceOf(address).call()
result2 = contract_instance.functions.allowance(SuperAccount,address).call()
print(str(result)+"#"+str(result2))
