import json
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import sys
import sqlite3
import os
Cpath = os.path.dirname(os.path.realpath(__file__))

host = "localhost"
contract_address = sys.argv[1]
prop = sys.argv[2]
prop = prop.replace("_yenkuanlee_"," ")
Plist = prop.split(",,,")
Pdict = dict()

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':3000'))
f = open(Cpath+'/abi','r')
abi = f.readline()
f.close()
abi = json.loads(abi)

contract_instance = w3.eth.contract(abi, contract_address, ContractFactoryClass=ConciseContract)
for i in range(len(Plist)):
    Pdict[Plist[i]] = int(contract_instance.GetVoteCount(i))
print(json.dumps(Pdict))
