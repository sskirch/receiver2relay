'''
Created on Dec 27, 2017

@author: sskirch
'''
import RPi.GPIO as GPIO


class trigger:
    GPIO_Pin = 0
    trigger_name = None
    trigger_status = None
    
    def __init__(self, trigger_name_in, GPIO_Pin_in):
        self.GPIO_Pin = GPIO_Pin_in
        self.trigger_name = trigger_name_in
        self.trigger_status = False
        GPIO.setup(self.GPIO_Pin, GPIO.OUT)
        
    def on(self):
        self.trigger_status = True
        GPIO.output(self.GPIO_Pin, GPIO.HIGH)
        
    def off(self):
        self.trigger_status = False
        GPIO.output(self.GPIO_Pin, GPIO.LOW)    
        
    def status(self):
        return self.trigger_status
                    

GPIO.setmode(GPIO.BCM)
