import json
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import sys
import os
from web3.middleware import geth_poa_middleware

Cpath = os.path.dirname(os.path.realpath(__file__))

host = "localhost"
contract_address = sys.argv[1]
behavior = sys.argv[2]

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':3000'))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)

f = open(Cpath+'/abi','r')
Aabi = f.readline()
f.close()
Aabi = json.loads(Aabi)

contract_instance = w3.eth.contract(abi=Aabi, address=contract_address)

if behavior == "winningProposal":
    print(contract_instance.functions.winningProposal().call())
elif behavior == "GetVoteCount":
    print(contract_instance.functions.GetVoteCount(int(sys.argv[3])).call())
elif behavior == "GetRemainVoteWeight":
    print(str(contract_instance.functions.GetRemainVoteWeight().call()))
