import json
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import sys
import os
Cpath = os.path.dirname(os.path.realpath(__file__))

host = "localhost"
account = "0x42946c2bb22ad422e7366d68d3ca07fb1862ff36"
passwd = "123"
contract_address = sys.argv[1]
to_Voter = sys.argv[2]
cnt = sys.argv[3]

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':3000'))
w3.personal.unlockAccount(account,passwd)
f = open(Cpath+'/abi','r')
abi = f.readline()
f.close()
abi = json.loads(abi)

# Contract instance in concise mode
contract_instance = w3.eth.contract(abi, contract_address, ContractFactoryClass=ConciseContract)

#w3.personal.unlockAccount(account, passwd)
contract_instance.vote(int(to_Voter),int(cnt),transact={'from': account})


