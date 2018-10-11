import json
import os
import requests
import sqlite3
import time
from datetime import datetime

APIURL = "localhost"
f = open('../../mcoin.conf','r')
while True:
    line = f.readline()
    if not line:
        break
    line = line.replace("\n","")
    line = line.replace(" ","")
    line = line.split("#")[0]
    try:
        tmp = line.split("=")
        if tmp[0]=="Lhost":
            APIURL = tmp[1]
    except:
        pass
f.close()
LusersPath = os.path.dirname(os.path.realpath(__file__))

def GetInfoBalance(Email):
    user_info = {"Email":Email}
    r = requests.post("http://"+APIURL+":5000/GetInfoX", data=user_info)
    Jr = json.loads(r.text)
    return Jr['Balance']

def LusersUpdate():
    Rlist = list()
    conn = sqlite3.connect(LusersPath+'/LocalUsers.db')
    c = conn.cursor()
    lusers = c.execute("SELECT * FROM Lusers;")
    for x in lusers:
        Rlist.append(x)
    for x in Rlist:
        c.execute("UPDATE Lusers set balance="+str(GetInfoBalance(x[0]))+" WHERE Email='"+x[0]+"'")
        conn.commit()
    conn.close()

while True:
    now = datetime.today()
    try:
        LusersUpdate()
        f = open('latest','w')
        f.write(str(now))
        f.close()
    except:
        time.sleep(10)
    time.sleep(10)
