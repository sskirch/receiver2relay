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
    def __init__(self, trigger_name_in, GPIO_Pin_in, expiration):
        self.expiration = expiration
        super(Beeper, self).__init__(trigger_name_in, GPIO_Pin_in)

    def on(self, on_seconds=60):
        triggers.trigger.on(self)
        self.expiration = on_seconds
        self.timestamp = time.time()

    def check_expire(self):
        if self.status() and (time.time() - self.timestamp) > self.expiration:
            triggers.trigger.off(self)
            return True
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
                sleep(0.2)
            triggers.trigger.on(self)
            sleep(0.2)
            triggers.trigger.off(self)
                


class Receiver():
	on = False
	timestamp = None
	click_count = 0
	pin = None
	sprink = None
	beep = None


	def __init__(self, pin, sprink, beep):
		self.pin = pin
		self.sprink = sprink
		self.beep = beep

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
                        			self.spring.on(300)
                        			self.beep.beeps(2)
                        			print(">1")

				elif self.click_count == 2 and not self.sprink.status():
					self.spring.on(600)
                    			self.beep.beeps(4)
					print(">2")
				elif self.click_count == 3 and not self.sprink.status():
					self.spring.on(1800)
					self.beep.beeps(6)
					print(">3")
				self.reset()


def loop():
	GPIO.cleanup()
	print("Started\n")

	sprink1 = triggers.trigger('One', 21)
	sprink2 = triggers.trigger('Two', 20)
	sprink3 = triggers.trigger('Three', 16)
	sprink4 = triggers.trigger('Four', 12)

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


if __name__ == '__main__':
	loop()

