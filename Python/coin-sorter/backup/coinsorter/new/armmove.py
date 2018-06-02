#!/usr/bin/python3
from time import sleep
import datetime ,os
from uf.wrapper.swift_api import SwiftAPI 
from uf.utils.log import *
import json
import cgi , cgitb


print("Content-type: application/json")
print()
form = cgi.FieldStorage()


swift = SwiftAPI()
sleep(2)
swift.set_buzzer()

try:
  os.remove("Armstatus.txt")
except OSError:
  pass

file =open('Armstatus.txt','w')
file.write('True')
file.close()

## Arm move controller
def armmove(x, y,toX ,toY):
   

   # global arm_speed
   global arm_speed
   arm_speed = 75
   
   swift.set_position(x, y, 100, arm_speed, relative=False, wait=True)
   sleep(1) 

   swift.set_position(x, y, 40, 5, relative=False, wait=True)
   sleep(1)

   swift.set_pump(True)
   sleep(1)

   swift.set_position(x, y, 100, arm_speed, relative=False, wait=True)
   sleep(1)

   swift.set_position(toX, toY, 100, arm_speed, relative=False, wait=True)
   sleep(1)

   swift.set_pump(False)
   sleep(1)
      

def main():
   with open('cord.txt','r') as fobj:
      lines = fobj.read().splitlines()
      for line in lines:       
          with open('Armstatus.txt','r') as status_obj:
              status = status_obj.read().strip()              
              if (status == 'True'):                 
                position = line.split(",")               

                if(position[2] == "25"):
                  armmove(position[1], position[0], -20, 250)      

                elif(position[2] == "5"):
                  ## print("taking 5 cent")
                  armmove(position[1], position[0], -20, 200)     

                elif(position[2] == "10"):
                  ## print("taking 10 cent")
                  armmove(position[1], position[0], -20, 150)      

                elif(position[2] == "1"):
                  ## print("taking 1 cent")
                  armmove(position[1], position[0], -20, 100)
              
              else:
                    break              
      
           
          
   response={}
   response["status"] = 200
   # response["count"] = count
   print(json.dumps(response))

   

main()
