# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 16:09:01 2017

@author: Jun Hao
"""

#Set print command to print to file
import sys
sys.stdout = open("Output.txt", "w")

#Print current time on computer
from datetime import datetime
print (str(datetime.now()))

#Implement simple timer
import time
current_milli_time = lambda: int(round(time.time() * 1000))
#startTime = current_milli_time()

import pandas as pd
import numpy as np
import csv
from sklearn import preprocessing
import serial


# Declarations
flag = 1
ignoreloopcount = 0
loopcount = 0
newAccID = 0
oldAccID = 0
oldTime = current_milli_time()
newTime = current_milli_time()
# Declare column headers
cols = ['accID', 'x0', 'y0', 'z0', 'x1', 'y1', 'z1', 'x2', 'y2', 'z2', 'x3', 'y3', 'z3', 'pwr', 'hash']
fullDF = pd.DataFrame(columns=cols)

# Initialize serial
ser = serial.Serial("/dev/ttyACM3", baudrate=9600, timeout=3.0)
print("Raspberry Pi Ready")

# Ignore first 20 readings
print("Ignoring starting readings")
while (ignoreloopcount < 20):
    while flag == 1:
        ser.write("\r\nH")
        print("H sent, awaiting response...")
        response = ser.read()
        if response == 'A':
            print("Response verified, handshake complete")
            print("Begin reading:")
            flag = 0
            ser.write("\r\nA")
    message = ser.readline()
    print(message)
    ignoreloopcount += 1
    ser.write("\r\nA")

# Read (Main Loop)
while (loopcount < 50):
    newTime = current_milli_time()
    message = ser.readline()
    newAccID = int(message.split(',')[0])
    if ((newAccID > oldAccID) & (newTime >= oldTime)):
        messagenp = np.fromstring(message, dtype=int, sep=",")
        messagepd = pd.DataFrame(data=messagenp.reshape(-1, len(messagenp)), index=['1'], columns=cols)
        print(messagepd)
        fullDF = fullDF.append(messagepd, ignore_index = True)
        loopcount += 1
        oldAccID = newAccID
        oldTime = newTime + 20 #20ms => 50Hz
        ser.write("\r\nA")

print(fullDF)
