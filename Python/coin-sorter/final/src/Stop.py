#!/usr/bin/python3
import datetime
import json
import cgi , cgitb

#Json content type
print("Content-type: application/json")
print()
form = cgi.FieldStorage()


#Writing False to File to stop arm movement
with open('../config/ArmStatus.txt','w') as wobj:
   wobj.write('False')


#Json response 
response={}
response["status"] = 200
# response["count"] = count
print(json.dumps(response))

