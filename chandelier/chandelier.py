import sys
from time import sleep
from chandelier import bt_devices, led, movement_sensor, pulseaudio
from .utilities import errprint
import threading


class Chandelier:
    standby_on = True
    def __init__(self, sensors_pins, led_pins, speaker_addr, remote_addr):
        self.blt_speaker = bt_devices.BluetoothSpeaker(speaker_addr, debug=False)
        self.remote = bt_devices.BluetoothRemote(remote_addr)
        self.sensors = movement_sensor.MovementSensors(sensors_pins)
        self.led = led.Led(led_pins[0], led_pins[1], led_pins[2])

    def play_ringtone(self, volume):
        self.ringtone = pulseaudio.Play(
            [(self.blt_speaker.pa_index, volume)], "../ringtone.mp3")

    def stop_playing_ringtone(self):
        self.ringtone.stop_playing()

    def play_voices(self, volume):
        self.svoices = pulseaudio.Play([(self.blt_speaker.pa_index, volume)], "../ambient1.wav")

    def stop_playing_voices(self):
        self.svoices.stop_playing()

    def led_white(self):
        self.led.set_r_intensity(100)
        self.led.set_g_intensity(100)

    def led_red(self):
        self.led.set_r_intensity(100)
        self.led.set_g_intensity(0)

    def __led_pulsing_white(self):
        while self.standby_on == True:
            for i in range(1, 155, 1):
                self.led.set_r_intensity(pow(1.03, i))
                self.led.set_g_intensity(pow(1.03, i))
                if self.standby_on == False:
                    return True
                sleep(0.03)

            for i in range(155, 1, -1):
                self.led.set_r_intensity(pow(1.03, i))
                self.led.set_g_intensity(pow(1.03, i))
                if self.standby_on == False:
                    return True
                sleep(0.03)

    def __led_pulsing_red(self):
        self.led.set_g_intensity(0)
        while self.standby_on == True:
            for i in range(1, 155, 1):
                self.led.set_r_intensity(pow(1.03, i))
                if self.standby_on == False:
                    return True
                sleep(0.03)

            for i in range(155, 1, -1):
                self.led.set_r_intensity(pow(1.03, i))
                if self.standby_on == False:
                    return True
                sleep(0.03)


    def wait_for_beggining(self):
        led_thread = threading.Thread(target=self.__led_pulsing_white)
        sensors_thread = threading.Thread(target=self.sensors.wait_for_movement)
        sensors_thread.start()
        led_thread.start()
        sensors_thread.join()
        self.standby_on = False
    
    def voices(self):
        led_thread = threading.Thread(target=self.__led_pulsing_red)
        self.play_voices(5)
        led_thread.start()
        result = self.wait_for_pick_up()
        self.stop_playing_voices()
        return result

    def wait_for_pick_up(self):
        butt_down = self.remote.wait_and_get_output()
        print(butt_down)
        while True:
            if butt_down.keystate == 1:
                while True:
                    butt_up = self.remote.wait_and_get_output()
                    if butt_up.keystate == 0:
                        if butt_up.event.sec - butt_down.event.sec >= 3:
                            return "long"
                        else:
                            return "short"



def main():

    chandelier = Chandelier([16, 26], [20, 21, 21],
                            "30:21:A0:29:85:28", "2A:07:98:10:34:2C") #sensors, leds, speaker, remote
    chandelier.wait_for_beggining()
    chandelier.led_white()
    sleep(3)
    chandelier.play_ringtone(1)
    print("dupa")
    chandelier.wait_for_pick_up()
    chandelier.stop_playing_ringtone()
    if chandelier.voices() == "short":
        print("you did it <3")
    