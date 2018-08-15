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
Cpath = os.path.dirname(os.path.realpath(__file__))

host = 'localhost'
TID = sys.argv[1]

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':3000'))
f = open(Cpath+'/abi','r')
line = f.readline()
Jline = json.loads(line)
f.close()

abi = Jline

Transaction = w3.eth.getTransaction(TID)
#print(Transaction.input)


def decode_contract_call(contract_abi: list, call_data: str):
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

result = decode_contract_call(abi,Transaction.input)
#result = decode_contract_call(abi,"0xa9059cbb0000000000000000000000006cd5d27785e38b28a0d9656bcc795d90a4d670c500000000000000000000000000000000000000000000000000000000000001f4")
print(result)
print(Transaction['from'])
