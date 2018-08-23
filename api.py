from flask import Flask
from flask import request
from flask_cors import CORS
import os
import requests
import subprocess
import json
import time
import hashlib

app = Flask(__name__)
CORS(app, resources=r'/*')

Lhost = '172.16.0.17'
SuperEmail = "yenkuanlee@gmail.com"
ProjectPath = "/home/localadmin/yenkuanlee/Mcoin"

@app.route('/kevin')
def index():
    args = request.args
    return args['key1']

@app.route('/Login', methods=['POST'])
def login():
    account = request.form['account']
    passwd = request.form['passwd']
    m = hashlib.md5()
    ts = str(int(time.time()))
    m.update(("MCU"+passwd+account+ts).encode('utf-8'))
    h = m.hexdigest()
    Odict = dict()
    Odict['account'] = account
    Odict['token'] = h
    Odict['timestamp'] = ts
    return json.dumps(Odict)

'''
@app.route('/SetUser')
def set_user():
    args = request.args
    Email = args['Email']
    Ehash = args['Ehash']
    StudentID = args['StudentID']
    role = args['role']
    
    user_info = {"Email":Email}
    try:
        r = requests.post("http://"+Lhost+":5000/GetInfo", data=user_info)
        if r.text != "ERROR" and "405 Method Not Allowed" not in r.text:
            return json.dumps({"status":r.text})
    except:
        return json.dumps({"status":"ERROR"})
    
    cmd = "python3 "+ProjectPath+"/User/EX/SetUser.py "+Email+" "+Ehash+" "+StudentID+" "+role
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode("utf-8")
    Odict = dict()
    Odict["status"] = "SUCCESS"
    Odict["TID"] = output.split("\n")[1]
    return json.dumps(Odict)
'''

@app.route('/SetUserX', methods=['POST'])
def set_userX():
    WhiteList = ['yenkuanlee@gmail.com','luhaoming@gmail.com']
    Email = request.form['Email']
    Ehash = request.form['Ehash']
    StudentID = request.form['StudentID']
    role = request.form['role']
    
    user_info = {"Email":Email}
    try:
        r = requests.post("http://"+Lhost+":5000/GetInfoX", data=user_info)
        if Email in WhiteList:
            pass
        elif r.text != "ERROR": # Not New Email
            Jr = json.loads(r.text)
            if Jr["TransactionRecord"]["Data"] == Email: # already existed
                return json.dumps({"status":"EmailAlreadyUsedException"})
    except Exception as e:
        return json.dumps({"status":e})

    cmd = "python3 "+ProjectPath+"/User/EX/SetUser.py "+Email+" "+Ehash+" "+StudentID+" "+role
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode("utf-8")
    Odict = dict()
    Odict["status"] = "SUCCESS"
    Odict["TID"] = output.split("\n")[1]
    return json.dumps(Odict)

@app.route('/GetInfo')
def get_info():
    args = request.args
    Email = args['Email']
    cmd = "python3 "+ProjectPath+"/User/EX/GetInfo.py "+Email
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode("utf-8")
    try:
        Joutput = json.loads(output)
    except:
        return ""
    Odict = dict()
    Odict['Ehash'] = Joutput[0]
    Odict['StudentID'] = Joutput[1]
    #Odict["IPFSHASH"] = Joutput[2]
    cmd = "timeout 10 ipfs object get "+Joutput[2]
    try:
        output = subprocess.check_output(cmd, shell=True)
    except:
        return "ERROR"
    output = output.decode("utf-8")
    transaction_record = json.loads(output)
    Odict['TransactionRecord'] = transaction_record
    Odict['role'] = Joutput[3]
    Odict['nounce'] = Joutput[4]
    cmd = "python3 "+ProjectPath+"/Balance/EX/GetBalance.py "+Odict['Ehash']
    try:
        output = subprocess.check_output(cmd, shell=True)
    except:
        return "ERROR"
    tmp = output.decode("utf-8").split("#")
    Odict['Balance'] = int(tmp[0])
    Odict['Allowance'] = int(tmp[1])
    return json.dumps(Odict)

@app.route('/GetInfoX', methods=['POST'])
def get_infoX():
    Email = request.form['Email']
    cmd = "python3 "+ProjectPath+"/User/EX/GetInfo.py "+Email
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode("utf-8")
    try:
        Joutput = json.loads(output)
    except:
        return ""
    Odict = dict()
    Odict['Ehash'] = Joutput[0]
    Odict['StudentID'] = Joutput[1]
    #Odict["IPFSHASH"] = Joutput[2]
    cmd = "timeout 10 ipfs object get "+Joutput[2]
    try:
        output = subprocess.check_output(cmd, shell=True)
    except:
        return "ERROR"
    output = output.decode("utf-8")
    transaction_record = json.loads(output)
    Odict['TransactionRecord'] = transaction_record
    Odict['role'] = Joutput[3]
    Odict['nounce'] = Joutput[4]
    cmd = "python3 "+ProjectPath+"/Balance/EX/GetBalance.py "+Odict['Ehash']
    try:
        output = subprocess.check_output(cmd, shell=True)
    except:
        return "ERROR"
    tmp = output.decode("utf-8").split("#")
    Odict['Balance'] = int(tmp[0])
    Odict['Allowance'] = int(tmp[1])
    return json.dumps(Odict)

@app.route('/GetBalance')
def get_balance():
    args = request.args
    Ehash = args['Ehash']
    cmd = "python3 "+ProjectPath+"/Balance/EX/GetBalance.py "+Ehash
    output = subprocess.check_output(cmd, shell=True)
    return output

@app.route('/GetBalanceX', methods=['POST'])
def get_balanceX():
    Ehash = request.form['Ehash']
    cmd = "python3 "+ProjectPath+"/Balance/EX/GetBalance.py "+Ehash
    output = subprocess.check_output(cmd, shell=True)
    return output

@app.route('/sendRawTransaction')
def send_raw_transaction():
    args = request.args
    RAW_TRANSACTION = args['RAW_TRANSACTION']
    cmd = "python3 "+ProjectPath+"/Transaction/EX/sendRawTransaction.py "+RAW_TRANSACTION
    output = subprocess.check_output(cmd, shell=True)
    return output

@app.route('/sendRawTransactionX', methods=['POST'])
def send_raw_transactionX():
    RAW_TRANSACTION = request.form['RAW_TRANSACTION']
    cmd = "python3 "+ProjectPath+"/Transaction/EX/sendRawTransaction.py "+RAW_TRANSACTION
    output = subprocess.check_output(cmd, shell=True)
    return output

@app.route('/CheckTransaction')
def check_transaction():
    args = request.args
    TID = args['TID']
    cmd = "python3 "+ProjectPath+"/Transaction/EX/CheckTransaction.py "+TID
    output = subprocess.check_output(cmd, shell=True)
    return output

@app.route('/CheckTransactionX', methods=['POST'])
def check_transactionX():
    TID = request.form['TID']
    cmd = "python3 "+ProjectPath+"/Transaction/EX/CheckTransaction.py "+TID
    output = subprocess.check_output(cmd, shell=True)
    return output

############################################################################################    
# Mvote
@app.route('/GetAppInfo')
def get_app_info():
    args = request.args
    App = args['App']
    cmd = "python3 "+ProjectPath+"/Application/GetAppInfo.py "+App
    output = subprocess.check_output(cmd, shell=True)
    tmp = output.decode("utf-8").split("\n")
    return tmp[len(tmp)-2]

@app.route('/Vote/GetTicketNumber')
def vote_get_ticket_number():
    args = request.args
    contract_address = args['contract_address']
    prop = args['prop']
    cmd = "python3 "+ProjectPath+"/Application/Vote/GetTicketNumber.py "+contract_address+" "+prop
    output = subprocess.check_output(cmd, shell=True)
    return output

@app.route('/Vote/SetVote')
def vote_set_vote():
    args = request.args
    topic = args['topic']
    prop = args['prop']
    deadline = args['deadline']
    number_of_prop = str(len(prop.split(",,,")))
    total_ticket = "10000"
    cmd = "python3 "+ProjectPath+"/Application/Vote/SetVote.py "+topic+" "+number_of_prop+" "+total_ticket+" "+prop+" "+deadline
    try:
        output = subprocess.check_output(cmd, shell=True)
        return "SUCCESS"
    except:
        return "ERROR"

@app.route('/Vote/DoVote')
def do_vote():
    args = request.args
    RAW_TRANSACTION = args['RAW_TRANSACTION']
    contract_address = args['contract_address']
    to_prop = args['to_prop']
    user_info = {"RAW_TRANSACTION":RAW_TRANSACTION}
    r = requests.post("http://"+Lhost+":5000/sendRawTransactionX", data=user_info)
    
    TID = json.loads(r.text)[0]
    user_info = {"TID":TID}
    r2 = requests.post("http://"+Lhost+":5000/CheckTransactionX", data=user_info)

    Jinfo = json.loads(r2.text)
    receiver = Jinfo['receiver']
    mcoin = Jinfo['mcoin']
    if receiver != SuperEmail:
        return json.dumps({"ERROR":TID})

    cmd = "python3 "+ProjectPath+"/Application/Vote/Vote.py "+contract_address+" "+to_prop+" "+str(mcoin)
    try:
        output = subprocess.check_output(cmd, shell=True)
        return "SUCCESS"
    except:
        return "ERROR"
    

## get all vote information : Mvote/Application/GetAppInfo.py
## make a vote : Mvote/Vote/SetVote.py
## do vote : Mvote/Vote/Vote.py
## see the status of one vote : Mvote/Vote/CheckVote.py
## see the result of one vote : Mvote/Vote/GetTicketNumber.py

if __name__ == '__main__':
    app.run(host=Lhost, debug=True)
