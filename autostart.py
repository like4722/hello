#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import datetime
import time
import psutil

#运行exe文件
def run():
    kill()
    os.chdir(r"C:\Users\atom\Desktop\FLVoutput\\")
    path = "FLPandSR.exe"
    print("运行FLPandSR.exe进程")
    os.system(path)

#杀掉进程
def kill():
    pids = psutil.pids()
    for pid in pids:
        p = psutil.Process(pid)
        #print(p.name())
        if p.name() == 'PCSE_TERM.exe':
            print("杀死PCSE_TERM.exe进程")
            cmd = 'taskkill /F /IM PCSE_TERM.exe'
            os.system(cmd)
        if p.name() == 'FLPandSR.exe':
            print("杀死FLPandSR.exe进程")
            cmd =  'taskkill /F /IM FLPandSR.exe'
            os.system(cmd)

def judge(h1=7,h2=10,h3=14):
    while True:
        now = datetime.datetime.now()
        print(now)
        # 每隔60分检测一次
        if now.hour == h1 or now.hour == h2 or now.hour == h3 :
            run()
        time.sleep(3600)
def main():
    judge()

if __name__ == '__main__':
    main()

