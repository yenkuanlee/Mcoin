from flask import Flask
from flask import request
from flask_cors import CORS
import json
import requests
import time

app = Flask(__name__)
CORS(app, resources=r'/*')
Lhost = '120.125.73.108'
SUdict = dict()

@app.route('/kevin', methods=['POST'])
def index():
    return request.form['key1']

@app.route('/MCUlogin', methods=['POST'])
def mcu_login():
    account = request.form['account']
    passwd = request.form['passwd']
    user_info = {'id':account, 'pw':passwd.upper()}
    url = 'https://tea.mcu.edu.tw/APPAPI/api/AILife/AILogin/'+account+'/'+passwd.upper()
    r = requests.post(url, data=json.dumps(user_info))
    Jr = json.loads(r.text)
    if Jr['Msg'] == "true":
        SUdict[account] = dict()
        SUdict[account]['status'] = True
        SUdict[account]['deadline'] = int(time.time())
    return r.text

@app.route('/GetSUstatus', methods=['POST'])
def get_set_user_status():
    account = request.form['account']
    nowTime = int(time.time())
    if account not in SUdict:
        return json.dumps({"status":False})
    if nowTime-SUdict[account]['deadline'] > 60:
        return json.dumps({"status":False})
    return json.dumps(SUdict[account])


if __name__ == '__main__':
    app.run(host=Lhost, debug=True)
