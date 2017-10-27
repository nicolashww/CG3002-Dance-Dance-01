import serial

ser = serial.Serial("/dev/ttyACM3", baudrate=9600, timeout=3.0)
flag = 1
print("Rpi ready")

while True:
	while flag == 1:
		ser.write("\r\nH")
		print("H sent")
		response = ser.read()
		if response == 'A':
			print("Handshake complete")
			flag = 0
			ser.write("\r\nA")

	message = ser.readline()
    
	accID = message.split(',')[0]
	xpos0 = message.split(',')[1]
	ypos0 = message.split(',')[2]
	zpos0 = message.split(',')[3]
	xpos1 = message.split(',')[4]
	ypos1 = message.split(',')[5]
	zpos1 = message.split(',')[6]
	xpos2 = message.split(',')[7]
	ypos2 = message.split(',')[8]
	zpos2 = message.split(',')[9]
	xpos3 = message.split(',')[10]
	ypos3 = message.split(',')[11]
	zpos3 = message.split(',')[12]
	#current = message.split(',')[13]
	print("ID: ", accID)
	print("xpos0: ", xpos0)
	print("ypos0: ", ypos0)
	print("zpos0: ", zpos0)
	ser.write("\r\nA")
	