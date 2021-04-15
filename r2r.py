#!/usr/bin/env python

import time
import math
import sys
from datetime import datetime, timedelta

import triggers
import sensors

class Receiver():
	on = False
	timestamp = None
	click_count = 0
	pin = None
	
	def __init__(self, pin):
		self.pin = pin
		
		
	def reset(self):
		self.on = False
		timestamp = None
		click_count = 0
			
	def check(self):
		now = int(time.time()) 
		if self.pin.check():  #If button down.
			self.on = True 
		elif self.on:  #If button is not down, but it used to be the last time we checked.
			if click_count > 0 and (now - self.timestamp) >= 2:  #If the last time we clicked was greater than two seconds 
				if click_count == 1:
					print(">1")
				elif click_count == 2:
					print(">3")
				elif click_count == 3:
					print(">3")
				self.reset()			
			else:  #If the last time we clicked was less than two seconds 
				self.click_count += 1
				self.timestamp = now
			
				
	 
	


def loop():
	print("Started\n")

	"""

	relay1 = triggers.trigger('One',21)
	relay2 = triggers.trigger('Two',20)
	relay3 = triggers.trigger('Three',16)
	relay4 = triggers.trigger('Four',12)

	while True:
		print "\n" + 'On 1'
		relay1.on()
		time.sleep(5)
		relay1.off()
		print "\n" + 'Off 1'

		print "\n" + 'On 2'
		relay2.on()
		time.sleep(5)
		relay2.off()
		print "\n" + 'Off 2'

		print "\n" + 'On 3'
		relay3.on()
		time.sleep(5)
		relay3.off()
		print "\n" + 'Off 3'

		print "\n" + 'On 4'
		relay4.on()
		time.sleep(5)
		relay4.off()
		print "\n" + 'Off 4'

	"""

	pin1 =  sensors.sensor("One", 14)
	pin2 =  sensors.sensor("Two", 15)
	pin3 =  sensors.sensor("Three", 18)
	pin4 =  sensors.sensor("Four", 23)
	
	r1 = Receiver(pin1)
	r2 = Receiver(pin2)
	r3 = Receiver(pin3)
	r4 = Receiver(pin4)

	while True:
		r1.check()
		r2.check()
		r3.check()
		r4.check()


if __name__ == '__main__':
	loop()







