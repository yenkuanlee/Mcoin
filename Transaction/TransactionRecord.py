# -*- coding: utf-8 -*-
import json
from web3 import Web3, HTTPProvider, TestRPCProvider
from web3.contract import ConciseContract
import os
import sys
import subprocess

def ObjectPeer(PeerID):
    cmd = "echo '{ \"Data\": \""+PeerID+"\" }' | ipfs object put"
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode("utf-8")
    PeerHash = output.split(" ")[1].split("\n")[0]
    return PeerHash

def AddHash(ObjectHash,Fhash,ObjectName):
    cmd = "timeout 10 ipfs object patch add-link "+ObjectHash+" "+ObjectName+" "+Fhash
    output = "OUTPUT ERROR"
    try:
        output = subprocess.check_output(cmd, shell=True)
        output = output.decode("utf-8")
        if "Error" in output:
            return ObjectHash
    except:
        return ObjectHash
    NewOhash = output.split("\n")[0]
    cmd = "timeout 10 ipfs pin add "+NewOhash
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode("utf-8")
    if "Error" in output:
        return ObjectHash
    return NewOhash

host = 'localhost'
account = '0x42946c2bb22ad422e7366d68d3ca07fb1862ff36'
passwd = '123'

Email = sys.argv[1]
tag = "123"

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':3000'))
w3.personal.unlockAccount(account,passwd)
f = open('../User/users.json','r')
line = f.readline()
Jline = json.loads(line)
f.close()

abi = Jline['abi']
contract_address = Jline['contract_address']


# Contract instance in concise mode
contract_instance = w3.eth.contract(abi, contract_address, ContractFactoryClass=ConciseContract)

result = contract_instance.GetInfo(Email)
ObjectHash = result[2]
T = sys.argv[2]
OT = ObjectPeer(T)
NewObjectHash = AddHash(ObjectHash,OT,T)
tag = NewObjectHash

contract_instance.setTag(Email,tag, transact={'from': account})
