import sys
from time import sleep
from chandelier import bt_devices, led, movement_sensor, pulseaudio
from .utilities import errprint
import asyncio

class Chandelier:
    def __init__(self, sensors_pins, led_pins, speaker_addr, remote_addr):
        #self.blt_speaker = bt_devices.BluetoothSpeaker(speaker_addr, debug=False)
        #self.remote = bt_devices.BluetoothRemote(remote_addr)
        #self.sensors = movement_sensor.MovementSensors(sensors_pins)
        self.led = led.Led(led_pins[0], led_pins[1], led_pins[2])

    def play_ringtone(self, volume):
        self.ringtone = pulseaudio.Play([(self.blt_speaker.pa_index, volume)], "axel.mp3")
    
    def stop_playing_ringtone(self):
        self.ringtone.stop_playing()
    
    def play_voices(self, volume):
        self.voices = pulseaudio.Play([(0, volume)], "../ambient1.wav")
    
    def stop_playing_voices(self):
        self.voices.stop_playing()

    def led_after_detection(self):
        self.led.set_r_intensity(100)
        self.led.set_g_intensity(100)
    
    def led_after_pick_up(self):
        self.led.set_r_intensity(100)
        self.led.set_g_intensity(0)
    
    def led_standby(self):
        while True:
            for i in range(1,48, 1):
                self.led.set_r_intensity(pow(1.01,i))
                self.led.set_g_intensity(pow(1.01,i))
                sleep(0.01)
            
            for i in range(48,1, -1):
                self.led.set_r_intensity(pow(1.01,i))
                self.led.set_g_intensity(pow(1.01,i))
                sleep(0.01)

    


def connect_to_speaker(addr, retry=10, debug=False):
    for i in range(1, retry):
        try:
            return bt_devices.BluetoothSpeaker(addr, debug=debug)
        except bt_devices.BluetoothSpeaker.DeviceNotFound:
            continue
        except Exception as exception:
            errprint('An exception occurred: %r', exception)
            sys.exit(10)


def manage_buttons(remote):
    while True:
        butt_down = remote.WaitAndGetOutput()
        if butt_down.keystate == 1:
            while True:
                butt_up = remote.WaitAndGetOutput()
                if butt_up.keystate == 0:
                    if butt_up.event.sec - butt_down.event.sec >= 5:
                        return "long"
                    else:
                        return "short"

def main():
    
    chandelier = Chandelier([19, 26], [20,21,21], "0C:A6:94:62:67:40", "2A:07:98:10:34:2C")
    #chandelier.play_ringtone(1)
    #chandelier.play_voices(1)
    #chandelier.led_after_detection()
    #sleep(10)
    #chandelier.led_after_pick_up()
    #sleep(10)
    chandelier.led_standby()
    #chandelier.sensors.wait_for_movement()


