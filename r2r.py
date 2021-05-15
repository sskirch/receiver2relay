#!/usr/bin/env python

import time
import math
import sys
from datetime import datetime, timedelta

import triggers
import sensors
import RPi.GPIO as GPIO


beep = None

class Beeper(triggers.trigger, object):
        timestamp = None
	expiration = 0

        def __init__(self, trigger_name_in, GPIO_Pin_in, expiration):
		self.expiration = expiration
		super(Beeper, self).__init__(trigger_name_in, GPIO_Pin_in)

	def on(self):
		triggers.trigger.on(self)
		self.timestamp = time.time()

	def check_expire(self):
		if self.status() and (time.time() - self.timestamp) > self.expiration:
			triggers.trigger.off(self)
			return True
		return False



class Receiver():
	on = False
	timestamp = None
	click_count = 0
	pin = None
	relay = None
	beep = None


	def __init__(self, pin, relay, beep):
		self.pin = pin
		self.relay = relay
		self.beep = beep

	def reset(self):
		self.on = False
		self.timestamp = None
		self.click_count = 0
			
	def check(self):
		now = time.time()
		if self.pin.check():  #If button down.
			if not self.on:
				self.click_count += 1
				self.on = True
				self.timestamp = now
				print("click " + self.pin.sensor_name)
				self.beep.on()

		elif self.on:  #If button is not down, but it used to be the last time we checked.
			self.on = False
			#print("let go")
		elif self.click_count > 0:
			#print("time now: " + str(now))
			#print("timestamp: " + str(self.timestamp))
			#print("click count: " + str(self.click_count))
			if (now - self.timestamp) >= 2:  #If the last time we clicked was greater than two seconds 
				#print("It's been two seconds")
				if self.click_count == 1:
					if self.relay.status():
						self.relay.off()
                                                print(self.relay.status())
						self.beep.off()
					else:
						self.relay.on()
                                                print(self.relay.status())

				elif self.click_count == 2:
					print(">2")
				elif self.click_count == 3:
					print(">3")
				self.reset()
			#else:  #If the last time we clicked was less than two seconds
				#print("It's been LESS THAN two seconds")


def loop():
	GPIO.cleanup()
	print("Started\n")

	relay1 = triggers.trigger('One',21)
	relay2 = triggers.trigger('Two',20)
	relay3 = triggers.trigger('Three',16)
	relay4 = triggers.trigger('Four',12)

	beep = Beeper('Beep',24,1)

	pin1 =  sensors.sensor("One", 14)
	pin2 =  sensors.sensor("Two", 15)
	pin3 =  sensors.sensor("Three", 18)
	pin4 =  sensors.sensor("Four", 23)
	
	r1 = Receiver(pin1, relay1, beep)
	r2 = Receiver(pin2, relay2, beep)
	r3 = Receiver(pin3, relay3, beep)
	r4 = Receiver(pin4, relay4, beep)

	print('Beep On')
	#GPIO.output(24, GPIO.HIGH)
	beep.on()
	#while not beep.check_expire():
	#	time.sleep(1)
	#	print('!')
	

	#GPIO.output(24, GPIO.HIGH)
	#beep.off()
	#print('Beep Off')
	

	try:
		while True:
			r1.check()
			beep.check_expire()
			r2.check()
			beep.check_expire()
			r3.check()
			beep.check_expire()
			r4.check()
			beep.check_expire()
	except KeyboardInterrupt:
    		pass

	GPIO.cleanup()	

if __name__ == '__main__':
	loop()







