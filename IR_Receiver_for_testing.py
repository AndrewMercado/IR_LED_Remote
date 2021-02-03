import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime

GPIO.setmode(GPIO.BCM)

REC = 18
LED = 20

GPIO.setup(REC, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

GPIO.output(LED,0)

code = []



def ConvertHex(BinVal): #Converts binary data to hexidecimal
	tmpB2 = int(str(BinVal), 2)
	return hex(tmpB2)




def conv_bin(code):
    binary = 1
    for (typ, tme) in code:
        if typ == 1:
            if tme > 0.001: #According to NEC protocol a gap of 1687.5 microseconds repesents a logical 1 so over 1000 should make a big enough distinction
                binary = binary * 10 + 1
            else:
                binary *= 10
				
    if len(str(binary)) > 34: #Sometimes the binary has two rouge charactes on the end
        binary = int(str(binary)[:34])
		
    return binary



def getData(): #Pulls data from sensor
	num1s = 0 #Number of consecutive 1s
	code = [] #Pulses and their timings
	previousValue = 0 #The previous pin state
	value = GPIO.input(REC) #Current pin state
	
	while value: #Waits until pin is pulled low
		value = GPIO.input(REC)
	
	startTime = datetime.now() #Sets start time
	
	while True:
		if value != previousValue: #Waits until change in state occurs
			now = datetime.now() #Records the current time
			pulseLength = now - startTime #Calculate time in between pulses
			startTime = now #Resets the start time
			code.append((previousValue, pulseLength.microseconds/1000000)) #Adds pulse time to array (previous val acts as an alternating 1 / 0 to show whether time is the on time or off time)
		
		#Interrupts code if an extended high period is detected (End Of Command)	
		if value:
			num1s += 1
		else:
			num1s = 0
		
		if num1s > 10000:
			return code
		
		#Reads values again
		previousValue = value
		value = GPIO.input(REC)
        




code = getData()

code_bin = conv_bin(code)
code_hex = ConvertHex(code_bin)


print(code)
print(code_bin)
print(code_hex)

input('Hit Enter...')

for i in range(1):
    
    for i in range(len(code)):
        if code[i][0]:
            GPIO.output(LED,0)
        else:
            GPIO.output(LED,1)
        sleep(code[i][1])
    sleep(.2)
   
GPIO.output(LED,0)



