import json
f = open("abi",'r')
line = f.readline()
Jline = json.loads(line)
print Jline
