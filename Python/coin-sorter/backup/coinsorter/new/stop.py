#!/usr/bin/python3
import datetime
import json
import cgi , cgitb

print("Content-type: application/json")
print()
form = cgi.FieldStorage()



with open('Armstatus.txt','w') as wobj:
   wobj.write('False')



response={}
response["status"] = 200
# response["count"] = count
print(json.dumps(response))

