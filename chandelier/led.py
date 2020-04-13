import RPi.GPIO as GPIO

class LedColor:
    pin = 0
    state = 1
    pwm = 0

    def __init__(self, pin):
        self.pin = pin

class Led:
    def __init__(self, G, B, R, freq=50):
        self._red = LedColor(R)
        self._green = LedColor(G)
        self._blue = LedColor(B)
        self.freq = freq
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self._red.pin, self._green.pin, self._blue.pin], GPIO.OUT)

        for color in [self._red, self._green, self._blue]:
            color.pwm = GPIO.PWM(color.pin, self.freq)
            color.pwm.start(0)

    def __del__(self):
        GPIO.cleanup([self._red.pin, self._green.pin, self._blue.pin])

    def __update_intensity__(self):
        pass

    def set_r_intensity(self, intensity=100):
        self._red.pwm.ChangeDutyCycle(intensity)

    def set_g_intensity(self, intensity=100):
        self._green.pwm.ChangeDutyCycle(intensity)

    def set_b_intensity(self, intensity=100):
        self._blue.pwm.ChangeDutyCycle(intensity)
