# -*- coding: utf-8 -*-
import json
from web3 import Web3, HTTPProvider, TestRPCProvider
from web3.contract import ConciseContract
import os
import sys
import ObjectNode
from web3.middleware import geth_poa_middleware
Cpath = os.path.dirname(os.path.realpath(__file__))

host = 'localhost'
account = '0x42946c2bb22ad422e7366d68d3ca07fb1862ff36'
passwd = '123'

Email = sys.argv[1]
Ehash = sys.argv[2]
StudentID = sys.argv[3]
Object = ObjectNode.ObjectNode(Email)
tag = Object.ObjectHash
role = sys.argv[4]

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':3000'))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)
account = w3.toChecksumAddress(account)
Email = w3.toBytes(text=Email)
w3.personal.unlockAccount(account,passwd)
f = open(Cpath+'/users.json','r')
line = f.readline()
Jline = json.loads(line)
f.close()

abi = Jline['abi']
contract_address = Jline['contract_address']


# Contract instance in concise mode
contract_instance = w3.eth.contract(abi=abi, address=contract_address)

#contract_instance.setNode(Email,Ehash,StudentID,tag,role, transact={'from': account})
contract_instance.functions.setNode(Email,w3.toChecksumAddress(Ehash),StudentID,tag,role).transact({'from': account})


#os.system("python3 /home/localadmin/yenkuanlee/Mcoin/Balance/Transfer.py "+Ehash+" 100")
###TID = w3.eth.sendTransaction({'to': Ehash, 'from': account, 'value': w3.toWei(100, "ether")})
###print(TID)
