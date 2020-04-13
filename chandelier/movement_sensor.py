import asyncio
from RPi import GPIO

class MovmentSensor():
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

    async def wait_for_movement(self):
        GPIO.wait_for_edge(SENSOR_PIN, GPIO.RISING)
        
    def __del__(self):
        GPIO.cleanup(self.pin)
