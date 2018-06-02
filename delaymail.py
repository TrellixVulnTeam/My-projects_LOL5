import boto3
from datetime import datetime, timedelta
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ['table1'])
table2 = dynamodb.Table(os.environ['table2'])
    
def lambda_handler(event, context):
    lastProcessedid = table.get_item(
        Key={
            'metaKey': 'lastProcessed'
        })
    totalItems = table.get_item(
        Key={
            'metaKey': 'totalItems'
        })
    lastProcessedid = lastProcessedid['Item']['metaValue']
    totalItems = totalItems['Item']['metaValue']
    print(lastProcessedid)
    print(totalItems)
    if(lastProcessedid != totalItems):
        print('init main')
        mainfun()

        
def mainfun():
    print("in main func")
    response = table.get_item(
        Key={
            'metaKey': 'lastProcessedDate'
        })
    lastProcessedTime = response['Item']['metaValue']
    currentTime       = (datetime.now()+timedelta(minutes=330)).strftime('%Y-%m-%d %H:%M:%S')
    print(lastProcessedTime)
    print(currentTime)
    FMT = '%Y-%m-%d %H:%M:%S'
    timediff = datetime.strptime(currentTime, FMT) - datetime.strptime(lastProcessedTime, FMT)
    print('currentTime')
    print(datetime.strptime(currentTime, FMT))
    print('lastProcessedTime')
    print(datetime.strptime(lastProcessedTime, FMT))
    print(timediff)
    print('timediff in seconds :')
    print(timediff.seconds)
    if(timediff.seconds > 600 and timediff.seconds <= 1200):
            alertmail()
    if(timediff.seconds > 1200):
            getemail()

   
def alertmail():
    print('alertmail fun')
    techemaillist = os.environ['techemaillist'].split(',')
    group = 'Tech'
    SendMail(techemaillist,group)
        
    #GET TODO MAIL ID
def getemail():
    print('in getmail fun')
    fe = Key('processStatus').eq('todo') & Key('delayMail').eq(False);
    response2 = table2.scan(
     FilterExpression=fe,
    )
    emaillist = []
    processIDlist =[]
    for i in response2['Items']:
        emailid= i['userEmail']
        processID = i['processId']
        emaillist.append(emailid)
        processIDlist.append(processID)
        
    emaillist = list(set(emaillist))
    group = 'User'
    if(emaillist):
        SendMail(emaillist,group)
    
    for id in processIDlist:
        updatetable = table2.update_item(
          Key={
          'processId': id
        },
        UpdateExpression="set delayMail =:r ",
        ExpressionAttributeValues={
             ':r': True
        })
    
    #SEND MAIL 
def SendMail(msgto,group):
    print('in  sendmail function')
    msg = MIMEMultipart()
    msg['From'] = os.environ['fromName']
    if(group == 'Tech'):
            msg['Subject'] = 'WhirlArt GPU ALERT !!'
            text = MIMEText(os.environ['techSubject'])
    else:
            msg['Subject'] = 'WhirlArt Notification'
            text = MIMEText(os.environ['userSubject'])
    msg.attach(text)
    s = smtplib.SMTP(os.environ['smtp'] , os.environ['smtpPort'])
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(os.environ['fromEmail'], os.environ['mailPassWord'])
    s.sendmail(msg['From'] ,  msgto, msg.as_string())
    print('mail sent')
    s.quit()

