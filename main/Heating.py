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
    
    while True:
        
        time.sleep( 1 )
        GPIO.output(7, 0) 
        time.sleep( 1 )
        GPIO.output(7, 1)   
        
        
 
if __name__ == '__main__':
    main()