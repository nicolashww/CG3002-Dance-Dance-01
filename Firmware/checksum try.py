import array
message = "test"
byteMessage = array.array('B', message)
print(byteMessage)
print(len(byteMessage))

i = 0
checkSum = 0

while i < (len(byteMessage)-1):
    checkSum ^= int(byteMessage[i])
    print(checkSum)
    print(i, ": ")
    print(message[i], "\n")
    i += 1

print(checkSum)
print(chr(checkSum))
print(hex(checkSum))

if chr(checkSum) == message[len(message)-1]:
    print('Correct')
    #Store data into buffer
else:
    print('Not Correct')
    #Send request for resend of data to Arduino
