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
f = open(Cpath+'/abi','r')
line = f.readline()
Jline = json.loads(line)
f.close()

abi = Jline
contract_address = "0x06E8b961683Ed5CE732748bF6bcaFF2aAedb689E"

# Contract instance in concise mode
contract_instance = w3.eth.contract(abi=abi, address=contract_address)

account = w3.toChecksumAddress("0x42946c2bb22ad422e7366d68d3ca07fb1862ff36")
passwd = "123"
w3.personal.unlockAccount(account,passwd)
address = w3.toChecksumAddress(sys.argv[1])
amount = int(sys.argv[2])
kk = contract_instance.functions.transfer(address,amount).transact({'from': account})
print(kk)
