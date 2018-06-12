# Mcoin
```
[ User ]
$ python3 /home/localadmin/yenkuanlee/Mcoin/User/SetUser.py yenkuanlee@gmail.com 0x42946c2bb22ad422e7366d68d3ca07fb1862ff36 F74982260 admin
$ curl "http://172.16.0.17:5000/SetUser?Email=yenkuanlee@gmail.com&Ehash=0x42946c2bb22ad422e7366d68d3ca07fb1862ff36&StudentID=F74982260&role=admin"

$ python3 /home/localadmin/yenkuanlee/Mcoin/User/GetInfo.py yenkuanlee@gmail.com
$ curl "http://172.16.0.17:5000/GetInfo?Email=yenkuanlee@gmail.com"


[ Balance ]
$ python3 /home/localadmin/yenkuanlee/Mcoin/Balance/GetBalance.py 0x42946c2bb22ad422e7366d68d3ca07fb1862ff36
$ curl "http://172.16.0.17:5000/GetBalance?Ehash=0x42946c2bb22ad422e7366d68d3ca07fb1862ff36"

python3 /home/localadmin/yenkuanlee/Mcoin/Balance/Transfer.py 0xe6ab871f860d9f28764d5d2e0672396a7643710e 1
# no api for security


[ Transaction ]
$ python3 /home/localadmin/yenkuanlee/Mcoin/Transaction/sendRawTransaction.py $RAW_TRANSACTION
$ curl "http://172.16.0.17:5000/sendRawTransaction?RAW_TRANSACTION=123234345"

$ python3 /home/localadmin/yenkuanlee/Mcoin/Transaction/TransactionRecord.py yenkuanlee@gmail.com A#B#1
$ curl "http://172.16.0.17:5000/TransactionRecord?Email=yenkuanlee@gmail.com&T=kevin800405@yahoo.com.tw#123"
```
