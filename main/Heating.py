'''
Created on May 25, 2016

@author: larsbremer
'''

import time
import logging
import logging.handlers
import RPi.GPIO as GPIO

class Heating(object):
    
        
    # Configure loggers
    logger = logging.getLogger('brewcontrol')
    logger.setLevel(logging.DEBUG)
    
    fh = logging.handlers.RotatingFileHandler('brew.log', mode='w', maxBytes='10000000', backupCount='5')
    fh.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler();
    ch.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    pin = 7
    interval = 5
    hysterese = 5
    targetTemp = 50
    heaterRunning = False


    
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
        
        logger.info('Turning heater on'+ str(heaterRunning))
        '''GPIO.output(pin, 0)'''
        heaterRunning = True
        logger.info('Turning heater on2'+ str(heaterRunning))
    
    
    def turnHeaterOff(self):
       
        logger.info('Turning heater off')
        '''GPIO.output(pin, 1)'''
        heaterRunning = False
    
    def __init__(self):
        
        logger.info('Gentlemen, start your engines!...')
    
        #Setup the pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT)
    
        while True:
            
            temp = readTemp()
            tempDelta = temp - targetTemp
            logger.info('Temperature is ' + str(temp) + ', target is ' + str(targetTemp) + ', difference is ' + str(tempDelta) + ', heater running ' + str(heaterRunning))
            
            if temp + hysterese < targetTemp and not heaterRunning:
                self.turnHeaterOn()
        elif temp - hysterese > targetTemp and heaterRunning:
                self.turnHeaterOff()
    
            time.sleep( interval )

if __name__ == '__main__':
    Heating()
