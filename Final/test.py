#!/usr/bin/python
#coding=utf-8
import RPi.GPIO as GPIO
import time
 
#回调函数
def callback(channel):
    print(GPIO.input(channel))
    if GPIO.input(channel):
        print(1)
    else:
        print(0)
 
#定义针脚排序为BOARD形式
GPIO.setmode(GPIO.BOARD)
 
#针脚
channel = 11
#定义针脚为input口
GPIO.setup(channel, GPIO.IN)
 
#添加简单事件
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=200)
#添加时间触发的回调函数
GPIO.add_event_callback(channel, callback)
 
#保持主进程不退出
while True:
    time.sleep(0.1)
    print(GPIO.input(channel))
    # if GPIO.input(channel):
    #     print(0)
    # else:
    #     print(1)