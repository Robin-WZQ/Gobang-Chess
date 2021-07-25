#!/usr/bin/python3
# coding=utf8
import sys
sys.path.append('/home/pi/ArmPi/')
import cv2
import time
import Camera
import threading
from LABConfig import *
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board
from CameraCalibration.CalibrationConfig import *

def init_position():
    Board.setBusServoPulse(5,700,1000)
    time.sleep(1)
    
    Board.setBusServoPulse(4, 800, 400) 
    time.sleep(0.5)
    
    Board.setBusServoPulse(6, 850, 400) 
    time.sleep(0.5) 

    Board.setBusServoPulse(3, 300, 300) 
    time.sleep(0.5) 

    Board.setBusServoPulse(2, 500, 300) 
    time.sleep(0.5) 

    Board.setBusServoPulse(1, 200, 300) 
    time.sleep(0.5) # 延时时间和运行时间相同

    Board.setBusServoPulse(1, 600, 1000) 
    time.sleep(2) # 延时时间和运行时间相同
    
def put_chess(x,y):
    AK.setPitchRangeMoving((x, y, 0.9), -90, -90, 0, 1000)
    time.sleep(2)
    Board.setBusServoPulse(1, 800, 500) 
    time.sleep(1)
    
def read_position():
    f = open("drop_point.txt", "r")
    x,y = f.read().split()
    f.close()
    return x,y

#x,y = read_position()
#print(x,y)

AK = ArmIK()
'''
init_position()
'''
while 1:
    x,y = input().split()
    put_chess(eval(x),eval(y))
