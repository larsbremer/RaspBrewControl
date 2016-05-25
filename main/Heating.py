'''
Created on May 25, 2016

@author: larsbremer
'''

import time
import RPi.GPIO as GPIO
   
def main():
    print 'Hello, world!'

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)

    pin = 7

    while True:

        time.sleep( 5 )
        GPIO.output(pin, 0)
        print "set pin " + str(pin) + " to low"
        time.sleep( 5 )
        GPIO.output(7, 1)
        print "set pin " + str(pin) + " to high"

        
        
 
if __name__ == '__main__':
    main()