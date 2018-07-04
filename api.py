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
    return "SUCCESS"

@app.route('/SetUserX', methods=['POST'])
def set_userX():
    Email = request.form['Email']
    Ehash = request.form['Ehash']
    StudentID = request.form['StudentID']
    role = request.form['role']
    os.system("python3 /home/localadmin/yenkuanlee/Mcoin/User/SetUser.py "+Email+" "+Ehash+" "+StudentID+" "+role)
    return "SUCCESS"

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
    Odict['nounce'] = Joutput[4]
    cmd = "python3 /home/localadmin/yenkuanlee/Mcoin/Balance/GetBalance.py "+Odict['Ehash']
    output = subprocess.check_output(cmd, shell=True)
    output = int(output.decode("utf-8"))
    Odict['Balance'] = output
    return json.dumps(Odict)

@app.route('/GetInfoX', methods=['POST'])
def get_infoX():
    Email = request.form['Email']
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
    Odict['nounce'] = Joutput[4]
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

@app.route('/GetBalanceX', methods=['POST'])
def get_balanceX():
    Ehash = request.form['Ehash']
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

@app.route('/sendRawTransactionX', methods=['POST'])
def send_raw_transactionX():
    RAW_TRANSACTION = request.form['RAW_TRANSACTION']
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

@app.route('/TransactionRecordX', methods=['POST'])
def transaction_recordX():
    Email = request.form['Email']
    T = request.form['T']
    cmd = "python3 /home/localadmin/yenkuanlee/Mcoin/Transaction/TransactionRecord.py "+Email+" "+T
    output = subprocess.check_output(cmd, shell=True)
    return output

if __name__ == '__main__':
    app.run(host='172.16.0.17', debug=True)
