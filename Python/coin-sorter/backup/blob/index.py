#!/usr/bin/python3
import coins_detect
import json
import cgi, cgitb
import time

import multiprocessing
import os
import signal

print("Content-type: application/json")
print()


form = cgi.FieldStorage()
method = form.getvalue('method')
urlq = form.getvalue('url')


def abort():
    f = open('RUNNING.txt', 'r')
    process = f.readline()
    process = filter(None, process.split(","))

    for p in process:
        os.kill(int(p), signal.SIGQUIT)

    f.close()
    os.remove('RUNNING.txt')
    response={}
    response["status"] = 200
    response["massage"] = "abort"
    print(json.dumps(response))

def mainqq():
    global urlq
    # print(urlq)

    f = open('RUNNING.txt', 'w')
    processes = []
    
    processes.append(multiprocessing.Process(target=coins_detect.main,args=(urlq,)))
    processes[-1].start()

    for p in processes:
        f.write(str(p.pid))
        f.write(",")
    f.close()
    response={}
    response["status"] = 200
    response["massage"] = "start"
    print(json.dumps(response))

if(method == "start"):
	# print("start")
	output, url, count=coins_detect.utility_capture(urlq)
	response={}
	response["status"] = output
	response["url"] = url
	response["count"] = count

	print(json.dumps(response))

elif(method == "main"):
	mainqq()

elif(method == "stop"):
	abort()






