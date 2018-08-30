import json
import requests
import sqlite3
import time
from datetime import datetime

APIURL = '172.16.0.17'
LusersPath = os.path.dirname(os.path.realpath(__file__))

def GetInfoBalance(Email):
    user_info = {"Email":Email}
    r = requests.post("http://"+APIURL+":5000/GetInfoX", data=user_info)
    Jr = json.loads(r.text)
    return Jr['Balance']

def LusersUpdate():
    Rlist = list()
    conn = sqlite3.connect(LusersPath+'LocalUsers.db')
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
    LusersUpdate()
    f = open('latest','w')
    f.write(str(now))
    f.close()
    time.sleep(10)
