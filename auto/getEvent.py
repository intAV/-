#coding=utf-8

import urllib2
import re
import time
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def getEvent():
    try:
        url = "https://www.bishijie.com/kuaixun.html";
        req = urllib2.Request(url)
        res_data = urllib2.urlopen(req)
        html = res_data.read()

        event = re.findall('<h2><a href="/kuaixun_(.*?)">', html, re.DOTALL)
        listEvent = []
        for list in event:
            title = list.split('title="')[1]
            listEvent.append(title)

        return listEvent[0]
    except:
        return "timeout."


def myPrint(content):
    newtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log = newtime+" "+content
    f = open(r'event.log', 'a')
    print >> f, "%s" % (log)
    print log.decode('utf8').encode('gbk')
    f.close()


def sendMail(context,title):
    _user = "cmdshell2@163.com"
    _pwd  = "5s9z6ws3su9r3"
    _to   = "1192769569@qq.com"

    msg = MIMEText(context)
    msg["Subject"] = title
    msg["From"]    = _user
    msg["To"]      = _to

    try:
        s = smtplib.SMTP_SSL("smtp.163.com", 465)
        s.login(_user, _pwd)
        s.sendmail(_user, _to, msg.as_string())
        s.quit()
        myPrint("send mail success")
    except Exception,e:
        myPrint("send mail error")



while True:
    myPrint("======================================================")
    oldEvent = getEvent()
    myPrint(oldEvent)

    time.sleep(120)

    newEvent = getEvent()
    myPrint(newEvent)

    if cmp(oldEvent,newEvent) != 0:
        #发现新快讯
        if "黑客" in newEvent:
            sendMail(newEvent,"警报")
        elif "攻击" in newEvent:
            sendMail(newEvent,"警报")
        elif "漏洞" in newEvent:
            sendMail(newEvent,"警报")
    else:
        myPrint("No")
    time.sleep(2)
