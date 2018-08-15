from web3 import Web3, HTTPProvider
import json
import os
import sys
import time
from web3.middleware import geth_poa_middleware

from ethereum.abi import (
    decode_abi,
    normalize_name as normalize_abi_method_name,
    method_id as get_abi_method_id)
from ethereum.utils import encode_int, zpad, decode_hex



Rhash = sys.argv[1]
Tlist = list()

w3 = Web3(HTTPProvider('http://localhost:3000'))
w3.middleware_stack.inject(geth_poa_middleware, layer=0)

tmp = Rhash.split(",")
for x in tmp:
    T = w3.eth.sendRawTransaction(x)
    Transaction = w3.eth.getTransaction(T)
    #print(Transaction.input)
    Tlist.append(str(T.hex()))


print(json.dumps(Tlist))

import InputDecoder
import datetime
for x in Tlist:
    a = InputDecoder.InputDecoder(x)
    Tinfo = a.Decoder()
    Tinfo['time'] = str(datetime.datetime.now())
    os.system("python3 /home/localadmin/yenkuanlee/Mcoin/Transaction/EX/TransactionRecord.py "+Tinfo['sender']+" "+json.dumps(Tinfo))
    os.system("python3 /home/localadmin/yenkuanlee/Mcoin/Transaction/EX/TransactionRecord.py "+Tinfo['receiver']+" "+json.dumps(Tinfo))
    #print(Tinfo['from'],Tinfo['to'],Tinfo['mcoin'],datetime.datetime.now())
    
