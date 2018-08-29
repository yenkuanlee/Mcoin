import io
import ipfsapi
import json
from web3 import Web3, HTTPProvider, TestRPCProvider
import os
from web3.middleware import geth_poa_middleware

SuperAccount = "0x42946c2bb22ad422e7366d68d3ca07fb1862ff36"
ERC20contract_address = "0x06E8b961683Ed5CE732748bF6bcaFF2aAedb689E"
ProjectPath = "/home/localadmin/yenkuanlee/Mcoin"
IPFS_IP = '127.0.0.1'
IPFS_PORT = 5001
Edict = dict()
Edict['User'] = ProjectPath+"/User/EX/users.json"
Edict['Application'] = ProjectPath+"/Application/app.json"
Edict['Balance'] = ProjectPath+"/Balance/EX/abi"

class EthWeb3Framework:
    def __init__(self, element):
        self.api = ipfsapi.connect(IPFS_IP,IPFS_PORT)
        self.w3 = Web3(HTTPProvider('http://localhost:3000'))
        self.w3.middleware_stack.inject(geth_poa_middleware, layer=0)
        f = open(Edict[element],'r')
        line = f.readline()
        Jline = json.loads(line)
        f.close()
        abi = Jline['abi']
        contract_address = Jline['contract_address']
        self.contract_instance = self.w3.eth.contract(abi=abi, address=contract_address)
        # ERC20 contract
        f = open(Edict['Balance'],'r')
        line = f.readline()
        Jline = json.loads(line)
        f.close()
        self.ERC20contract_instance = self.w3.eth.contract(abi=Jline, address=ERC20contract_address)

    def GetBalance(self,Ehash):
        try:
            address = self.w3.toChecksumAddress(Ehash)
            result = self.ERC20contract_instance.functions.balanceOf(address).call()
            return result
        except:
            return "GetBalanceFailed"
    def GetAllowance(self,Ehash):
        try:
            SuperAccountX = self.w3.toChecksumAddress(SuperAccount)
            address = self.w3.toChecksumAddress(Ehash)
            result = self.ERC20contract_instance.functions.allowance(SuperAccountX,address).call()
            return result
        except:
            return "GetAllowanceFailed"

    def GetInfo(self,Email):
        Odict = dict()
        try:
            Email = self.w3.toBytes(text=Email)
            result = self.contract_instance.functions.GetInfo(Email).call()
            Odict['Ehash'] = result[0]
            Odict['StudentID'] = result[1]
            try:
                Odict['TransactionRecord'] = self.api.object_get(result[2])
            except:
                Odict['TransactionRecord'] = "GetTransactionRecordFailed"
            Odict['role'] = result[3]
            try:
                nounce = self.w3.eth.getTransactionCount(self.w3.toChecksumAddress(Odict['Ehash']))
                Odict['nounce'] = nounce
            except:
                Odict['nounce'] = "GetNonceFailed"
            Odict['Balance'] = self.GetBalance(Odict['Ehash'])
            Odict['Allowance'] = self.GetAllowance(Odict['Ehash'])
            return Odict
        except Exception as e:
            return {"status":"GetInfoFailed", "log":str(e)}

    def SetUser(self,Email,Ehash,StudentID,role):
        account = self.w3.toChecksumAddress(SuperAccount)
        #Tbyte = bytes(json.dumps({"Data":Email}))
        Tbyte = json.dumps({"Data":Email}).encode()
        Email = self.w3.toBytes(text=Email)
        Ehash = self.w3.toChecksumAddress(Ehash)
        tag = self.api.object_put(io.BytesIO(Tbyte))['Hash']
        self.api.pin_add(tag)
        self.w3.personal.unlockAccount(account,"123")
        self.contract_instance.functions.setNode(Email,Ehash,StudentID,tag,role).transact({'from': account})
        TID = self.w3.eth.sendTransaction({'to': Ehash, 'from': account, 'value': self.w3.toWei(100, "ether")})
        return {"status":"SUCCESS"}
