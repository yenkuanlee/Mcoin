from flask import Flask
from flask import request
from flask_cors import CORS
import os
import requests
import subprocess
import json
import time
import hashlib
import ipfsapi
import io
import sqlite3
import EthWeb3Framework

app = Flask(__name__)
CORS(app, resources=r'/*')

Cpath = os.path.dirname(os.path.realpath(__file__))
f = open(Cpath+'/mcoin.conf','r')
Cdict = dict()
while True:
    line = f.readline()
    if not line:break
    line = line.replace("\n","")
    line = line.replace(" ","")
    line = line.split("#")[0]
    try:
        tmp = line.split("=")
        Cdict[tmp[0]] = tmp[1]
    except:
        pass
f.close()

Lhost = Cdict['Lhost']
SuperEmail = Cdict['SuperEmail']
ProjectPath = Cdict['ProjectPath']
IPFS_IP = Cdict['IPFS_IP']
IPFS_PORT = Cdict['IPFS_PORT']
PicturePath = Cdict['PicturePath']
PictureBias = Cdict['PictureBias']
LusersPath = Cdict['LusersPath']

@app.route('/kevin', methods=['POST'])
def index():
    return request.form['key1']

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

@app.route('/SetUserX', methods=['POST'])
def set_userX():
    Email = request.form['Email']
    Ehash = request.form['Ehash']
    StudentID = request.form['StudentID']
    role = request.form['role']
    try:
        Name = request.form['Name']
    except:
        Name = request.form['Email']
    a = EthWeb3Framework.EthWeb3Framework()
    result = a.SetUser(Email,Ehash,StudentID,role,Name)
    return json.dumps(result)

@app.route('/GetInfoX', methods=['POST'])
def get_infoX():
    Email = request.form['Email']
    a = EthWeb3Framework.EthWeb3Framework()
    return json.dumps(a.GetInfo(Email))

@app.route('/sendRawTransactionX', methods=['POST'])
def send_raw_transactionX():
    RAW_TRANSACTION = request.form['RAW_TRANSACTION']
    a = EthWeb3Framework.EthWeb3Framework()
    result = a.sendRawTransaction(RAW_TRANSACTION)
    return json.dumps(result)

@app.route('/CheckTransactionX', methods=['POST'])
def check_transactionX():
    TID = request.form['TID']
    a = EthWeb3Framework.EthWeb3Framework()
    result = a.CheckTransaction(TID)
    return json.dumps(result)

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

@app.route('/Vote/PictureStore', methods=['POST'])
def picture_store():
    bcode = request.form['bcode']
    ts = str(time.time())
    fw = open(PicturePath+PictureBias+ts,'w')
    fw.write(bcode)
    fw.close()
    api = ipfsapi.connect(IPFS_IP,IPFS_PORT)
    result = api.add(PicturePath+PictureBias+ts)
    os.system("mv "+PicturePath+PictureBias+ts+" "+PicturePath+result['Hash'])
    return result['Hash']

@app.route('/Vote/PictureGet', methods=['POST'])
def picture_get():
    phash = request.form['phash']
    api = ipfsapi.connect(IPFS_IP,IPFS_PORT)
    return api.cat(phash).decode('utf-8')
    
############################################################################################
##Lusers

@app.route('/Lusers/GetLusers', methods=['POST'])
def get_lusers():
    ResultList = list()
    conn = sqlite3.connect(LusersPath+'LocalUsers.db')
    c = conn.cursor()
    c.execute("create table if not exists Lusers(Email text, balance int, status int, PRIMARY KEY(Email));")
    try:
        c.execute("SELECT * FROM Lusers;")
        #conn.commit()
        for x in c:
            ResultList.append({"Email":x[0], "balance":x[1], "status":x[2]})
    except:
        return json.dumps({"status":"GetLusersFailed"})
    return json.dumps(ResultList)

@app.route('/Lusers/SetLusersStatus', methods=['POST'])
def set_lusers_status():
    Email = request.form['Email']
    status = request.form['status'][0]
    conn = sqlite3.connect(LusersPath+'LocalUsers.db')
    c = conn.cursor()
    try:
        a = EthWeb3Framework.EthWeb3Framework()
        result = a.SetUserStatus(Email,status)
        c.execute("UPDATE Lusers SET status="+status+" WHERE Email = '"+Email+"';")
        conn.commit()
        return json.dumps({"status":"SUCCESS"})
    except:
        return json.dumps({"status":"SetLusersStatusFailed"})

@app.route('/Lusers/GetLatestUpdateTime', methods=['POST'])
def get_lusers_update_time():
    try:
        f = open(ProjectPath+'/User/DB/latest','r')
        line = f.readline()
        line = line.replace("\n","")
        return json.dumps({"status":"SUCCESS", "latest":line})
    except:
        return json.dumps({"status":"GetLatestUpdateTimeFailed"})

if __name__ == '__main__':
    app.run(host=Lhost, debug=True)
