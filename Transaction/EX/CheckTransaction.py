import InputDecoder
import json
import sys
x = InputDecoder.InputDecoder(sys.argv[1])
result = x.Decoder()
Rdict = dict()
Rdict['sender'] = result[0]
Rdict['receiver'] = result[1]
Rdict['mcoin'] = result[2]
print(json.dumps(Rdict).replace("\\u0000",""))

