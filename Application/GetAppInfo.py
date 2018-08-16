import json
import subprocess
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import sys
import os
import ObjectNode
from web3.middleware import geth_poa_middleware

application = sys.argv[1]

# Set Peer
MCU = ObjectNode.ObjectNode("MCU")
accountPeer = MCU.ObjectPeer("account")
propPeer = MCU.ObjectPeer("prop")
deadlinePeer = MCU.ObjectPeer("deadline")

# Set Index
IndexDict = dict()
IndexDict[accountPeer] = "account"
IndexDict[propPeer] = "prop"
IndexDict[deadlinePeer] = "deadline"

Cpath = os.path.dirname(os.path.realpath(__file__))

host = 'localhost'
account = '0x42946c2bb22ad422e7366d68d3ca07fb1862ff36'
passwd = '123'

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':3000'))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)
account = w3.toChecksumAddress(account)
w3.personal.unlockAccount(account,passwd)
f = open(Cpath+'/app.json','r')
line = f.readline()
Jline = json.loads(line)
f.close()

abi = Jline['abi']
contract_address = Jline['contract_address']


# Contract instance in concise mode
contract_instance = w3.eth.contract(abi=abi, address=contract_address)
application = w3.toBytes(text=application)
AppHash = contract_instance.functions.GetOhash(application).call()
cmd = "timeout 10 ipfs object get "+AppHash
output = subprocess.check_output(cmd, shell=True)
Joutput = json.loads(output.decode("utf-8"))

Jlist = list()
for x in Joutput['Links']:
    Jdict = dict()
    Jdict['contract_address'] = x['Name']
    cmd = "timeout 10 ipfs object get "+x['Hash']
    print(x['Hash'])
    output = subprocess.check_output(cmd, shell=True)
    J = json.loads(output.decode("utf-8"))
    Jdict['topic'] = J['Data']
    for y in J['Links']:
        Jdict[IndexDict[y['Hash']]] = y['Name']
    Jlist.append(Jdict)
    #print(Jdict)

print(json.dumps(Jlist))
