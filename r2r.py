#!/usr/bin/env python

import time
import math
import sys
from datetime import datetime, timedelta

import triggers
import sensors


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

	while True:
		if pin1.check():
			print("one!")
		if pin2.check():
			print("two!")
		if pin3.check():
			print("three!")
		if pin4.check():
			print("four!")



if __name__ == '__main__':
	loop()







