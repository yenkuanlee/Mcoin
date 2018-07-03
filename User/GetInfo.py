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
f = open(Cpath+'/users.json','r')
line = f.readline()
Jline = json.loads(line)
f.close()

abi = Jline['abi']
contract_address = Jline['contract_address']

# Contract instance in concise mode
contract_instance = w3.eth.contract(abi, contract_address, ContractFactoryClass=ConciseContract)

Email = sys.argv[1]
result = contract_instance.GetInfo(Email)
nounce = w3.eth.getTransactionCount(result[0])
result.append(str(nounce))
print(json.dumps(result))
#print(json.dumps(contract_instance.GetInfo(Email)))
