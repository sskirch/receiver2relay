#!/usr/bin/env python

import time
import math
import sys
from datetime import datetime, timedelta

import triggers
import sensors
import RPi.GPIO as GPIO


beep = None

class Sprinkler(triggers.trigger, object):
	timestamp = None
	def __init__(self, trigger_name_in, GPIO_Pin_in):
        	self.expiration = 60
        	super(Sprinkler, self).__init__(trigger_name_in, GPIO_Pin_in)

	def on(self, on_seconds=60):
        	triggers.trigger.on(self)
	        self.expiration = on_seconds
        	self.timestamp = time.time()

	def check_expire(self):
		if self.status() and (time.time() - self.timestamp) > self.expiration:
			triggers.trigger.off(self)
			return True
		print(str(self.trigger_name) + ' ' + str(self.trigger_status))
		return False


class Beeper(triggers.trigger, object):
    timestamp = None
    
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
        
    def beeps(self, number_of_beeps):
        for i in range(0,number_of_beeps):
            if i !=0:
                time.sleep(0.1)
            triggers.trigger.on(self)
            time.sleep(0.1)
            triggers.trigger.off(self)
                


class Receiver():
	on = False
	timestamp = None
	click_count = 0


	def __init__(self, pin, sprink, beep):
		self.pin = pin
		self.sprink = sprink
		self.beep = beep
		self.click_count = 0

	def reset(self):
		self.on = False
		self.timestamp = None
		self.click_count = 0

	def check(self):
		now = time.time()
	        self.sprink.check_expire()

		if self.pin.check():  # If button down.
			if not self.on:
				self.click_count += 1
				self.on = True
				self.timestamp = now
				print("click " + self.pin.sensor_name)
				self.beep.beeps(1)
		elif self.on:  # If button is not down, but it used to be the last time we checked.
			self.on = False
		elif self.click_count > 0:
			if (now - self.timestamp) >= 2:  # If the last time we clicked was greater than two seconds 
				if self.click_count == 1:
					if self.sprink.status():
						self.sprink.off()
                        			print(self.sprink.status())
                        			self.beep.beeps(1)
						self.reset()
                    			else:
                        			self.sprink.on(15)
                        			self.beep.beeps(2)
                        			print(">1")

				elif self.click_count == 2 and not self.sprink.status():
					self.sprink.on(600)
                    			self.beep.beeps(4)
					print(">2")
				elif self.click_count == 3 and not self.sprink.status():
					self.sprink.on(1800)
					self.beep.beeps(6)
					print(">3")
				self.reset()


def loop():
	GPIO.cleanup()
	print("Started\n")

	sprink1 = Sprinkler('One', 21)
	sprink2 = Sprinkler('Two', 20)
	sprink3 = Sprinkler('Three', 16)
	sprink4 = Sprinkler('Four', 12)

	beep = Beeper('Beep', 24, 1)

	pin1 = sensors.sensor("One", 14)
	pin2 = sensors.sensor("Two", 15)
	pin3 = sensors.sensor("Three", 18)
	pin4 = sensors.sensor("Four", 23)

	r1 = Receiver(pin1, sprink1, beep)
	r2 = Receiver(pin2, sprink2, beep)
	r3 = Receiver(pin3, sprink3, beep)
	r4 = Receiver(pin4, sprink4, beep)

	try:
		while True:
			r1.check()
			r2.check()
			r3.check()
			r4.check()
	except KeyboardInterrupt:
		pass

	try:
        	GPIO.cleanup()
		print("Clean Exit")
	except:
		pass


	
def all_on(time_length=60):
	sprink1 = Sprinkler('One', 21)
	sprink2 = Sprinkler('Two', 20)
	sprink3 = Sprinkler('Three', 16)
	sprink4 = Sprinkler('Four', 12)

	sprink1.on(time_length)
	sprink2.on(time_length)
	sprink3.on(time_length)
	sprink4.on(time_length)

	try:
		while True:
			if sprink1.check_expire() and sprink2.check_expire() and sprink3.check_expire() and sprink4.check_expire():
				print('Done')
				exit()
			time.sleep(0.1)
	except KeyboardInterrupt:
		pass
	

def relay_on(relay, time_length=60):
	sprinklers = [ 
	{'One', 21},
	{'Two', 20},
	{'Three', 16},
	{'Four', 12}
	]	
	
	sprink = sprinklers[relay]
	sprink.on(time_length)

	try:
		while True:
			if sprink.check_expire():
				print('Done')
				exit()
			time.sleep(0.1)
	except KeyboardInterrupt:
		pass
	
	

if __name__ == '__main__':
	GPIO.cleanup()
	time_length = None  #time in seconds
	relay = None
	all = False
	if len(sys.argv) > 0:
		for a in sys.argv:
			if '-r' in a:
				relay = a.split('-r')[1]
				try: 
					relay = int(relay)
				except:
					print('Invalid argument: ' + str(a))
					exit()
				if relay < 0 or relay > 3:
					print('Invalid argument: ' + str(a))
					exit()
			elif '-t' in a:
				time_length = a.split('-t')[1]
				try: 
					time_length = int(relay)
				except:
					print('Invalid argument: ' + str(a))
					exit()
			elif '-a' == a:
				all = True
				
	if all and time_length:
		all_on(time_length)
	elif relay:
		relay_on(relay, time_length)
	
	
	
	
	
	#loop()

