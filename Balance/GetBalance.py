import json
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import sys
import os
Cpath = os.path.dirname(os.path.realpath(__file__))

host = 'localhost'

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':3000'))
f = open(Cpath+'/abi','r')
line = f.readline()
Jline = json.loads(line)
f.close()

abi = Jline
contract_address = "0x06E8b961683Ed5CE732748bF6bcaFF2aAedb689E"

# Contract instance in concise mode
contract_instance = w3.eth.contract(abi, contract_address, ContractFactoryClass=ConciseContract)

address = sys.argv[1]
result = contract_instance.balanceOf(address)
print(result)
