#import asyncio
from time import sleep
from RPi import GPIO

#class _SingleMovementSensor():
#    def __init__(self, pin, loop):
#        self.loop = loop
#        self.pin = pin
#        GPIO.setmode(GPIO.BCM)
#        GPIO.setup(self.pin, GPIO.IN)
#
#    def _add_movement_callback(self, callback):
#        GPIO.add_event_detect(self.pin, GPIO.RISING, callback)
#
#    def _remove_callback(self):
#        GPIO.remove_event_detect(self.pin)
#
#    def __del__(self):
#        GPIO.cleanup(self.pin)
#
#
#class MovementSensors():
#    def __init__(self, pin_list):
#        self.loop = asyncio.new_event_loop()
#        self.sensors = []
#        for pin in pin_list:
#            self.sensors.append(_SingleMovementSensor(pin, self.loop))
#    
#    def __stop_on_movement__(self, channel):
#        print(channel)
#        self.loop.call_soon_threadsafe(self.loop.stop)
#
#    def wait_for_movement(self):
#        for sensor in self.sensors:
#            sensor._add_movement_callback(self.__stop_on_movement__)
#        self.loop.run_forever()
#        self.loop.close()
#
#        for sensor in self.sensors:
#            sensor._remove_callback()
#
        
class _SingleMovementSensor():
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)
    def check_status(self):
        return GPIO.input(self.pin)

class MovementSensors():
    def __init__(self, pin_list):
        self.sensors = []
        for pin in pin_list:
            self.sensors.append(_SingleMovementSensor(pin))
    
    def wait_for_movement(self):
        while True:
            for sensor in self.sensors:
                if sensor.check_status() == 1:
                    print(sensor.pin)
                    return True
            sleep(0.25)
