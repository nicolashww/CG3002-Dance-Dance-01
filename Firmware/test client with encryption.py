from Crypto.Cipher import AES
from Crypto import Random
import base64
import os, random
import socket

client = socket.socket()
ip = input("Enter IP: ")
#ip = socket.gethostbyname(socket.gethostname())
port = int(input("Enter port: "))
#port = 3002
address = (ip,port)
client.connect(address)

def encryptData(data):
    BLOCK_SIZE = 16
    PADDING = ' '
    
    pad = lambda s: s + (BLOCK_SIZE - (len(s) % BLOCK_SIZE)) * PADDING

    key = '3002300230023002'
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encoded = base64.b64encode(iv + cipher.encrypt(pad(data)))
    #print('Encryption key: ', key)
    print('Encrypted string: ', encoded)
    return encoded

def sendEncoded(action, voltage, current, power, cumpower):
    msg = '#' + action + '|' + str(voltage) + '|' + str(current) + '|' + str(power) + '|' + str(cumpower)
    client.send(encryptData(msg))
