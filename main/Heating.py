'''
Created on May 25, 2016

@author: larsbremer
'''

import time
import logging
import logging.handlers
import RPi.GPIO as GPIO

class Heating(object):

    def readTemp(self):
        
        tfile = open("/sys/bus/w1/devices/28-00000555e0ae/w1_slave") 
        text = tfile.read() 
        tfile.close() 
        secondline = text.split("\n")[1] 
        temperaturedata = secondline.split(" ")[9] 
        temperature = float(temperaturedata[2:]) 
        temperature = temperature / 1000 
        return temperature
    
    def turnHeaterOn(self):
        
        self.logger.info('Turning heater on')
        GPIO.output(self.pin, 0)
        self.heaterRunning = True
    
    def turnHeaterOff(self):
       
        self.logger.info('Turning heater off')
        GPIO.output(self.pin, 1)
        self.heaterRunning = False
    
    def __init__(self):
        
        # Configure loggers
        self.logger = logging.getLogger('brewcontrol')
        self.logger.setLevel(logging.DEBUG)
        
        fh = logging.handlers.RotatingFileHandler('brew.log', mode='w', maxBytes='10000000', backupCount='5')
        fh.setLevel(logging.DEBUG)
        
        ch = logging.StreamHandler();
        ch.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        
        self.logger.info('Gentlemen, start your engines!...')
        
        self.pin = 7
        self.interval = 5
        self.hysterese = 5
        self.targetTemp = 50
        self.heaterRunning = False
    
        #Setup the pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
    
        while True:
            
            temp = self.readTemp()
            
            logString = 'Temperature is ' + str("%.2f" % temp)
            logString += ', target is ' + str(self.targetTemp)
            logString += ', heater is ' + ('on' if self.heaterRunning else 'off')
            
            self.logger.info(logString)
            
            if temp + self.hysterese < self.targetTemp and not self.heaterRunning:
                self.turnHeaterOn()
            elif temp - self.hysterese > self.targetTemp and self.heaterRunning:
                self.turnHeaterOff()
    
            time.sleep( self.interval )

if __name__ == '__main__':
    Heating()
