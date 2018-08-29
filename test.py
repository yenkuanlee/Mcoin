import EthWeb3Framework
Email = "yenkuanlee@gmail.com"
Ehash = "0x42946C2Bb22ad422e7366d68d3Ca07fB1862ff36"
StudentID = "F74982260"
role = "admin"

a = EthWeb3Framework.EthWeb3Framework("User")

print(a.GetInfo(Email))

#print(a.GetBalance("0x42946C2Bb22ad422e7366d68d3Ca07fB1862ff36"))
#print(a.GetAllowance("0x42946C2Bb22ad422e7366d68d3Ca07fB1862ff36"))
#print(a.SetUser(Email,Ehash,StudentID,role))
