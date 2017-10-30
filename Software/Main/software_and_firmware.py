# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 16:09:01 2017

@author: Jun Hao
"""

#Set print command to print to file
import sys
sys.stdout = open("OutputComb.txt", "w")

#Print current time on computer
from datetime import datetime
print (str(datetime.now()))

#Implement simple timer
import time
current_milli_time = lambda: int(round(time.time() * 1000))
#startTime = current_milli_time()

import pandas as pd
import numpy as np
#import csv
#from sklearn import preprocessing
import serial


# Declarations
flag = 1
ignoreloopcount = 0
loopcount = 0
newAccID = 0
oldAccID = 0
oldTime = current_milli_time()
newTime = current_milli_time()
hashcount = 0
checkSum = 0
# Declare column headers
cols = ['ID', 'x0', 'y0', 'z0', 'x1', 'y1', 'z1', 'x2', 'y2', 'z2', 'x3', 'y3', 'z3', 'chk']
fullDF = pd.DataFrame(columns=cols)

# Initialize serial
ser = serial.Serial("/dev/ttyACM3", baudrate=9600, timeout=3.0)
print("Raspberry Pi Ready")

# Perform handshake
while flag == 1:
        ser.write("\r\nH")
        print("H sent, awaiting response...")
        response = ser.read()
        if response == 'A':
            print("Response verified, handshake complete")
            print("Begin reading:")
            flag = 0
            ser.write("\r\nA")

# Ignore first 20 readings
print("Ignoring starting readings")
while (ignoreloopcount < 20):
    message = ser.readline()
    byteMessage = message.encode('utf-8')
    while hashcount < (len(byteMessage)-1): # Produce checksum from received data
        checkSum ^= byteMessage[hashcount]
        print(checkSum)
        print(hashcount, ": ")
        print(message[hashcount], "\n")
        hashcount += 1
    if chr(checkSum) == message[len(message)-1]: #Check if checksums matches
        print('Correct')
        print(message)
        ser.write("\r\nA")
        # Store data into buffer
    else: # Checksums do not match
        print('Not Correct')
        print(message)
        ser.write("\r\nR") # Send request for resend of data to Arduino
    ignoreloopcount += 1
    ser.write("\r\nA")

# Read (Main Loop)
while (loopcount < 50):
    message = ser.readline()
    newAccID = int(message.split(',')[0])
    if (newAccID == oldAccID):
        if chr(checkSum) == message[len(message)-1]: # Check if checksums matches
            print('Correct')
            messagenp = np.fromstring(message, dtype=int, sep=",")
            messagepd = pd.DataFrame(data=messagenp.reshape(-1, len(messagenp)), index=['1'], columns=cols)
            print(messagepd)
            ser.write("\r\nA")
            fullDF = fullDF.append(messagepd, ignore_index = True)
            loopcount += 1
            oldAccID = newAccID + 1
        else: # Checksums do not match
            print('Not Correct')
            print(message)
            ser.write("\r\nR") # Send request for resend of data to Arduino
    else :
        print('oldAccID = ' + oldAccID)
        print('newAccID = ' + newAccID)
        loopcount = 50


print(fullDF)


# Remove unneeded data
fullDF = fullDF.drop(fullDF.columns[14], axis=1)
fullDF = fullDF.drop(fullDF.columns[13], axis=1)
fullDF = fullDF.drop(fullDF.columns[0], axis=1)
# Save cleaned raw data to csv file
fullDF.to_csv('recorded_data.csv', sep=',')
