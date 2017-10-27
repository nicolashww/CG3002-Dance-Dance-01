# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 16:09:01 2017

@author: Jun Hao
"""

import pandas as pd
import numpy as np
#import csv
#from sklearn import preprocessing
import serial

#Declare empty dataframe
fullDF = pd.DataFrame(columns = ['accID', 'x0', 'y0', 'z0', 'x1', 'y1', 'z1', 'x2', 'y2', 'z2', 'x3', 'y3', 'z3', 'pwr'])

ser = serial.Serial("/dev/ttyACM3", baudrate=9600, timeout=3.0)
flag = 1
loopcount = 0
print("Raspberry Pi Ready")

while (loopcount<10):
    while flag == 1:
        ser.write("\r\nH")
        print("H sent")
        response = ser.read()
        if response == 'A':
            print("Handshake complete")
            flag = 0
            ser.write("\r\nA")
    message = ser.readline()
    messagenp = np.fromstring(message, dtype=int, sep=",")
    messagepd = pd.DataFrame(data=messagenp.reshape(-1, len(messagenp)), index=['1'], columns=['accID', 'x0', 'y0', 'z0', 'x1', 'y1', 'z1', 'x2', 'y2', 'z2', 'x3', 'y3', 'z3', 'pwr'])
    print(messagepd)
    fullDF = fullDF.append(messagepd, ignore_index = True)
    loppcount = loopcount + 1
    ser.write("\r\nA")

print(fullDF)
    