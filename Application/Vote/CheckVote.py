import json
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import sys
import os
Cpath = os.path.dirname(os.path.realpath(__file__))

host = "localhost"
contract_address = sys.argv[1]
behavior = sys.argv[2]

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':3000'))
f = open(Cpath+'/abi','r')
abi = f.readline()
f.close()
abi = json.loads(abi)

contract_instance = w3.eth.contract(abi, contract_address, ContractFactoryClass=ConciseContract)

if behavior == "winningProposal":
    print(contract_instance.winningProposal())
elif behavior == "GetVoteCount":
    print(contract_instance.GetVoteCount(int(sys.argv[3])))
elif behavior == "GetRemainVoteWeight":
    print(str(contract_instance.GetRemainVoteWeight()))
