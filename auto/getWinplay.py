#!/usr/bin/python
#coding=utf-8
import hackhttp
import re
import time
import datetime

hh = hackhttp.hackhttp()

count = 4

def getNumber():
    try:
        code, head, html, redirect, log = hh.http('https://mainnet.eoscanada.com/v1/chain/get_table_rows', post='{"code":"eoswinplayio","scope":"eoswinplayio","table":"lotrounds","index_position":"2","key_type":"i64","json":true,"limit":50}')
        if code == 200:
            number = re.findall('result":(.*?),', html, re.DOTALL)
            numtime = re.findall('"done":(.*?)}', html, re.DOTALL)

            i = 20
            xiao = 0
            da = 0
            while i > 0:
                endnum = int(number[i]) % 10
                if endnum < 5:
                    xiao = xiao + 1
                else:
                    xiao = 0
                if endnum > 4:
                    da = da + 1
                else:
                    da = 0

                putstr = "%d : %s  xiao:%d  da:%d  %s"%(i,number[i].zfill(5),xiao,da,time.strftime("%H:%M:%S", time.localtime(int(numtime[i]))))
                print putstr

                if i == 1:
                    if xiao > count:
                        print "[xiao] OK...."
                    if da > count:
                        print "[da] OK...."

                i = i - 1

            print "---------------------------------"
            #return time.strftime("%M", time.localtime(int(numtime[1])))

        else:
            print "error:"+html
    except:
        print "time out..."


while True:
    now_s = datetime.datetime.now().strftime('%S')
    #print now_s
    if now_s == "00" or now_s == "01" or now_s == "02" or now_s == "03" or now_s == "04" or now_s == "05" or now_s == "06" or now_s == "07":
        getNumber()
        time.sleep(1)
    time.sleep(1)
