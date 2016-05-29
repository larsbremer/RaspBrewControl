'''
Created on May 25, 2016

@author: larsbremer
'''

import time
import logging.handlers
import ConfigParser
import sys
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
    
    def turnHeaterOff(self):
       
        self.logger.info('Turning heater off')
        GPIO.output(self.pin, 1)
    
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
        
        config = ConfigParser.RawConfigParser()
        config.read('config.properties')

        self.pin = config.getint('Heater', 'heater.pin');
        self.interval = config.getint('Heater', 'heater.interval');
        self.hysterese = config.getint('Heater', 'heater.hysterese');
        self.targetTemp = config.getint('Heater', 'heater.targettemp');
    
        #Setup the pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
    
        while True:
            
            temp = self.readTemp()
            heaterRunning = not bool(GPIO.input(self.pin));
            
            logString = 'Temperature is ' + str("%.2f" % temp)
            logString += ', target is ' + str(self.targetTemp)
            logString += ', heater is ' + ('on' if heaterRunning else 'off')
            
            self.logger.info(logString)
            
            if temp + self.hysterese < self.targetTemp and not heaterRunning:
                self.turnHeaterOn()
            elif temp - self.hysterese > self.targetTemp and heaterRunning:
                self.turnHeaterOff()
    
            time.sleep( self.interval )

if __name__ == '__main__':

    try:
        Heating()
    except KeyboardInterrupt:
        GPIO.cleanup()
        sys.exit(0)
