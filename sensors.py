'''
Created on Dec 5, 2016

@author: sskirch
'''
import RPi.GPIO as GPIO
import os
import time


#Class to handle sensor on the PCF8591 ADDA.  Or anything that just uses one GPIO
class sensor:
    GPIO_Pin = 0
    
    def __init__(self, sensor_name_in, GPIO_Pin_in):
        self.sensor_name = sensor_name_in
        self.GPIO_Pin = GPIO_Pin_in
        GPIO.setup(GPIO_Pin_in, GPIO.IN)
        
    def check(self):  
        if GPIO.input(self.GPIO_Pin) == 1:
		return True
	else:
		return False

GPIO.setmode(GPIO.BCM)
