# -*- coding: utf-8 -*-
import json
from web3 import Web3, HTTPProvider, TestRPCProvider
from web3.contract import ConciseContract
import os
import sys
import subprocess
from web3.middleware import geth_poa_middleware

class Trecord:
    def __init__(self,_Email):
        Cpath = os.path.dirname(os.path.realpath(__file__))
        host = 'localhost'
        self.account = '0x42946c2bb22ad422e7366d68d3ca07fb1862ff36'
        passwd = '123'
        self.Email = _Email
        tag = "123"

        # web3.py instance
        self.w3 = Web3(HTTPProvider('http://'+host+':3000'))
        self.w3.middleware_stack.inject(geth_poa_middleware, layer=0)
        self.account = self.w3.toChecksumAddress(self.account)
        self.w3.personal.unlockAccount(self.account,passwd)
        f = open(Cpath+'/../../User/EX/users.json','r')
        line = f.readline()
        Jline = json.loads(line)
        f.close()

        abi = Jline['abi']
        contract_address = Jline['contract_address']
        # Contract instance in concise mode
        self.contract_instance = self.w3.eth.contract(abi=abi, address=contract_address)

    '''
    def ObjectPeer(self,PeerID):
        cmd = "echo '{ \"Data\": \""+PeerID+"\" }' | ipfs object put"
        output = subprocess.check_output(cmd, shell=True)
        output = output.decode("utf-8")
        PeerHash = output.split(" ")[1].split("\n")[0]
        return PeerHash

    def AddHash(self,ObjectHash,Fhash,ObjectName):
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
    '''

    def record(self,T):
        result = self.contract_instance.functions.GetInfo(self.w3.toBytes(text=self.Email)).call()
        ObjectHash = result[2]
        import ObjectNode
        x = ObjectNode.ObjectNode()
        x.load(ObjectHash)
        y = ObjectNode.ObjectNode()
        y.new(T)
        x.AddHash(T,y.ObjectHash)
        tag = x.ObjectHash

        TID = self.contract_instance.functions.setTag(self.w3.toBytes(text=self.Email),tag).transact({'from': self.account})
        return TID.hex()
