from ethereum.abi import (
    decode_abi,
    normalize_name as normalize_abi_method_name,
    method_id as get_abi_method_id)
from ethereum.utils import encode_int, zpad, decode_hex

import json
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract
import sys
import os
from web3.middleware import geth_poa_middleware

class InputDecoder:
    def __init__(self,_TID):
        self.Cpath = os.path.dirname(os.path.realpath(__file__))
        host = 'localhost'

        # web3.py instance
        self.w3 = Web3(HTTPProvider('http://'+host+':3000'))
        self.w3.middleware_stack.inject(geth_poa_middleware, layer=0)
        f = open(self.Cpath+'/abi','r')
        line = f.readline()
        Jline = json.loads(line)
        f.close()

        self.abi = Jline

        self.Transaction = self.w3.eth.getTransaction(_TID)
        #self.w3.eth.waitForTransactionReceipt(_TID)
        #tx_receipt = self.w3.eth.getTransactionReceipt(_TID)
        #print(tx_receipt)


    def decode_contract_call(self,contract_abi: list, call_data: str):
        call_data_bin = decode_hex(call_data)
        method_signature = call_data_bin[:4]
        for description in contract_abi:
            if description.get('type') != 'function':
                continue
            method_name = normalize_abi_method_name(description['name'])
            arg_types = [item['type'] for item in description['inputs']]
            method_id = get_abi_method_id(method_name, arg_types)
            if zpad(encode_int(method_id), 4) == method_signature:
                try:
                    args = decode_abi(arg_types, call_data_bin[4:])
                except AssertionError:
                    # Invalid args
                    continue
                return method_name, args

    def Decoder(self):
        result = self.decode_contract_call(self.abi,self.Transaction.input)
        if result[0]!="transfer" and result[0]!="transferFrom":
            return "NotTransferException"
        Rdict = dict()
        Rdict['sender'] = self.UserMapping(self.Transaction['from'])
        Rdict['receiver'] = self.UserMapping(result[1][0])
        Rdict['mcoin'] = result[1][1]
        return [self.UserMapping(self.Transaction['from']).decode("utf-8"),self.UserMapping(result[1][0]).decode("utf-8"),result[1][1]]

    def UserMapping(self,Ehash):
        f = open(self.Cpath+'/../../User/EX/users.json','r')
        line = f.readline()
        Jline = json.loads(line)
        f.close()
        Uabi = Jline['abi']
        Ucontract_address = Jline['contract_address']
        contract_instance = self.w3.eth.contract(abi=Uabi, address=Ucontract_address)
        Ehash = self.w3.toChecksumAddress(Ehash)
        return contract_instance.functions.GetUserMapping(Ehash).call()
