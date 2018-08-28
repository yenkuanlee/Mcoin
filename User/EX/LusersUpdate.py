import json
import requests
import sqlite3

APIURL = '172.16.0.17'
LusersPath = "/home/localadmin/yenkuanlee/Mcoin/User/EX/"

def GetInfoBalance(Email):
    user_info = {"Email":Email}
    r = requests.post("http://"+APIURL+":5000/GetInfoX", data=user_info)
    Jr = json.loads(r.text)
    return Jr['Balance']

conn = sqlite3.connect(LusersPath+'LocalUsers.db')
c = conn.cursor()
c.execute("SELECT * FROM Lusers;")
for x in c:
    c.execute("UPDATE Lusers set balance="+str(GetInfoBalance(x[0]))+" WHERE Email='"+x[0]+"'")
    conn.commit()
