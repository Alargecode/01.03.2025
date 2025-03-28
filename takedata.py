import serial
import time
import string
import sys
from time import sleep

sys.setrecursionlimit(10000)
ser = serial.Serial('/dev/ttyUSB0', 9600,timeout=0.5)
#ser = 37

class data:
	def take_data():
		return ser
	def take_data():
		kast = 0
		val=ser.read(1) 
		val +=ser.read(8)
		k = 0
		power = 0
		#print(val)
		for i in range(9):
			if (val[i] == 45 or val[i] == 43):
				k = i + 1
				for m in range(7):
					if(k == 9):
						k = 0
					else:
						if(val[k] == 46):
							k = k+1
						elif(val[k] == 13):
							k = k+1
						else:
							kast = kast + (val[k] - 48)*(10000/(10**power))
							power = power + 1
							#print(val[k])
							k = k + 1
		if kast == 0:
			return 1
		else:
			return int(kast)
	
	def close():
		ser.flushInput()
		ser.flushOutput()
		sleep(0.1)
		
