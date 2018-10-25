# coding=utf-8
import EthWeb3Framework
import sys

#Email = "yenkuanlee@gmail.com"
Email = 't1@ee.com'
Ehash = "0x42946C2Bb22ad422e7366d68d3Ca07fB1862ff36"
StudentID = "F74982260"
role = "admin"
Name = "李彥寬"

a = EthWeb3Framework.EthWeb3Framework()

print(a.GetInfo(Email))

##print(a.GetBalance(Ehash))
##print(a.GetAllowance(Ehash))

#print(a.SetUser(Email,Ehash,StudentID,role,Name))
#print(a.SetUserStatus(Email,"0"))
#print(a.UserMapping(Ehash))

#print(a.Trecord(Email,"666"))
#print(a.sendRawTransaction(sys.argv[1]))
#print(a.CheckTransaction(sys.argv[1]))
