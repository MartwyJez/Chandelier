import RPi.GPIO as GPIO
import time

GB = 21
R = 20
 
GPIO.setmode(GPIO.BCM)
GPIO.setup(GB, GPIO.OUT)
GPIO.setup(R, GPIO.OUT)

GPIO.output(R, 1)
GPIO.output(GB, 0)
GPIO.cleanup()