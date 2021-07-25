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
import torch


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

    Board.setBusServoPulse(1, 700, 1000) 
    time.sleep(2) # 延时时间和运行时间相同
    
def put_chess(x,y):
    result = AK.setPitchRangeMoving((x, y, 0.05*y+1.5), -90, -90, 0, 2000)
    time.sleep(3)
    #print(result[0]['servo5'])
    Board.setBusServoPulse(2, 400, 500)
    time.sleep(1)
    '''Board.setBusServoPulse(5, result[0]['servo5']-(30-y), 500)
    time.sleep(0.5)'''
    Board.setBusServoPulse(4, result[0]['servo4']+20, 500)
    time.sleep(0.5)
    Board.setBusServoPulse(3, result[0]['servo3']+20, 500)
    time.sleep(0.5)
    '''Board.setBusServoPulse(5, result[0]['servo5']+20, 500)
    time.sleep(0.5)
    Board.setBusServoPulse(4, result[0]['servo4']+20, 500)
    time.sleep(0.5)'''
    Board.setBusServoPulse(1, 300, 2000) 
    time.sleep(3)
    Board.setBusServoPulse(5, 800, 2000)
    #write_data(result[0]['servo3'],result[0]['servo4'],result[0]['servo5'],result[0]['servo6'])
    time.sleep(3)
    return result[0]
    
def read_position():
    f = open("drop_point.txt", "r")
    x,y = f.read().split()
    f.close()
    return x,y

def read_data():
    '''
    读入数据
    '''
    position = open("/home/pi/ArmPi/play_the_chess/position.txt",mode='r')
    p = position.readlines()
    for i in range(len(p)):
        k=p[i].strip('\n').split()
        re = put_chess(float(k[0]),float(k[1]))
        write_data(re['servo3'],re['servo4'],re['servo5'],re['servo6'])
    position.close()
    return 0

def write_data(x1,x2,x3,x4):
    '''
    构造训练集
    '''
    f = open("/home/pi/ArmPi/play_the_chess/train.txt",mode='a')
    f.write(str(x1)+' ')
    f.write(str(x2)+' ')
    f.write(str(x3)+' ')
    f.write(str(x4)+'\n')
    f.close
    return 0

def put_chess2(x,y):
    #load the pre-trained model
    model = network()
    model.load_state_dict(torch.load("my_model.pth"))
    model.eval()
    p = model(torch.tensor([[x,y]]).float())
    #run the arm
    Board.setBusServoPulse(3, int(p[0][0].trunc()), 500)
    time.sleep(1)
    Board.setBusServoPulse(4, int(p[0][1].trunc()), 500)
    time.sleep(1)
    Board.setBusServoPulse(5, int(p[0][2].trunc()), 500)
    time.sleep(1)
    Board.setBusServoPulse(6, int(p[0][3].trunc()), 500)
    time.sleep(3)
    #fine tuning
    Board.setBusServoPulse(2, 400, 500)
    time.sleep(1)
    Board.setBusServoPulse(4, int(p[0][1].trunc())+20, 500)
    time.sleep(0.5)
    Board.setBusServoPulse(3, int(p[0][0].trunc())+20, 500)
    time.sleep(0.5)
    Board.setBusServoPulse(1, 300, 2000) 
    time.sleep(3)
    Board.setBusServoPulse(5, 800, 2000)
    time.sleep(3)

#x,y = read_position()
#print(x,y)

AK = ArmIK()
#read_data()

#init_position()
    
#put_chess(0,20)
