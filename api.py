from flask import Flask
from flask import request
import os
import subprocess
import json

app = Flask(__name__)

@app.route('/kevin')
def index():
    args = request.args
    return args['key1']

@app.route('/SetUser')
def set_user():
    args = request.args
    Email = args['Email']
    Ehash = args['Ehash']
    StudentID = args['StudentID']
    role = args['role']
    os.system("python3 /home/localadmin/yenkuanlee/Mcoin/User/SetUser.py "+Email+" "+Ehash+" "+StudentID+" "+role)
    return "good"

@app.route('/GetInfo')
def get_info():
    args = request.args
    Email = args['Email']
    cmd = "python3 /home/localadmin/yenkuanlee/Mcoin/User/GetInfo.py "+Email
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode("utf-8")
    Joutput = json.loads(output)
    Odict = dict()
    Odict['Ehash'] = Joutput[0]
    Odict['StudentID'] = Joutput[1]
    #Odict["IPFSHASH"] = Joutput[2]
    cmd = "timeout 10 ipfs object get "+Joutput[2]
    output = subprocess.check_output(cmd, shell=True)
    output = output.decode("utf-8")
    transaction_record = json.loads(output)
    Odict['TransactionRecord'] = transaction_record
    Odict['role'] = Joutput[3]
    cmd = "python3 /home/localadmin/yenkuanlee/Mcoin/Balance/GetBalance.py "+Odict['Ehash']
    output = subprocess.check_output(cmd, shell=True)
    output = int(output.decode("utf-8"))
    Odict['Balance'] = output
    return json.dumps(Odict)

@app.route('/GetBalance')
def get_balance():
    args = request.args
    Ehash = args['Ehash']
    cmd = "python3 /home/localadmin/yenkuanlee/Mcoin/Balance/GetBalance.py "+Ehash
    output = subprocess.check_output(cmd, shell=True)
    return output

@app.route('/sendRawTransaction')
def send_raw_transaction():
    args = request.args
    RAW_TRANSACTION = args['RAW_TRANSACTION']
    cmd = "python3 /home/localadmin/yenkuanlee/Mcoin/Transaction/sendRawTransaction.py "+RAW_TRANSACTION
    output = subprocess.check_output(cmd, shell=True)
    return output

@app.route('/TransactionRecord')
def transaction_record():
    args = request.args
    Email = args['Email']
    T = args['T']
    cmd = "python3 /home/localadmin/yenkuanlee/Mcoin/Transaction/TransactionRecord.py "+Email+" "+T
    output = subprocess.check_output(cmd, shell=True)
    return output

if __name__ == '__main__':
    app.run(host='172.16.0.17', debug=True)
