import json
import os
import time
from web3 import Web3, HTTPProvider, TestRPCProvider
from solc import compile_source
from web3.contract import ConciseContract

host = 'localhost'
account = '0x42946c2bb22ad422e7366d68d3ca07fb1862ff36'
passwd = '123'

f = open('app.sol','r')
X = ""
while True:
    line = f.readline()
    if not line:
        break
    X += line
contract_source_code = X

compiled_sol = compile_source(contract_source_code) # Compiled source code
contract_interface = compiled_sol['<stdin>:App']

# web3.py instance
w3 = Web3(HTTPProvider('http://'+host+':3000'))
account = w3.toChecksumAddress(account)
w3.personal.unlockAccount(account, passwd)
# Instantiate and deploy contract
contractt = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Get transaction hash from deployed contract
tx_hash = contractt.deploy(transaction={'from': account, 'gas': 4000000})
###print(tx_hash)

# Get tx receipt to get contract address
tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

cnt = 1
while True:
	if tx_receipt == None:
		print("wait...("+str(cnt)+")")
		cnt += 1
		time.sleep(1)
		tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
	else:
		break

###print(tx_receipt)
contract_address = tx_receipt['contractAddress']

# Contract instance in concise mode
contract_instance = w3.eth.contract(abi=contract_interface['abi'], address=contract_address)

Joutput = dict()
fw = open('app.json','w')
Joutput['abi'] = contract_interface['abi']
Joutput['contract_address'] = contract_address
fw.write(json.dumps(Joutput))
fw.close()

os.system("echo '{ \"Data\": \"Vote\" }' | ipfs object put")

print("account : "+account)
print("contract address : "+contract_address)
print("contract abi : "+json.dumps(contract_interface['abi']))

