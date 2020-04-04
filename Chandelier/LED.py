#import RPi.GPIO as GPIO
#import time
#
#GB = 36
#R = 40   
# 
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(GB, GPIO.OUT)
#GPIO.setup(R, GPIO.OUT)
#
#
#GPIO.gpio_function(OUT)
#
##def my_callback(channel):
##    # Here, alternatively, an application / command etc. can be started.
##    print('There was a movement!')
## 
##try:
##    GPIO.add_event_detect(SENSOR_PIN , GPIO.RISING, callback=my_callback)
##    while True:
##        time.sleep(1)
##except KeyboardInterrupt:
##    print('Finish...')
#GPIO.cleanup()