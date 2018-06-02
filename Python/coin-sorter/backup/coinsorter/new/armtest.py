#!/usr/bin/python3
from time import sleep
import datetime
from uf.wrapper.swift_api import SwiftAPI 
from uf.utils.log import *
import json
import cgi , cgitb


print("Content-type: application/json")
print()
form = cgi.FieldStorage()

swift = SwiftAPI()
sleep(2)
swift.set_position(100, 200, 100, 70, relative=False, wait=True)



response={}
response["status"] = 200
# response["count"] = count
print(json.dumps(response))
