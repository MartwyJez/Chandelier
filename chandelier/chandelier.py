import sys
from time import sleep
from chandelier import bt_devices, led, movement_sensor, pulseaudio
from .utilities import errprint
import threading


class Chandelier:
    standby_on = True
    def __init__(self, sensors_pins, led_pins, speaker_addr, remote_addr):
        self.blt_speaker = bt_devices.BluetoothSpeaker(speaker_addr, debug=False)
        #self.remote = bt_devices.BluetoothRemote(remote_addr)
        self.sensors = movement_sensor.MovementSensors(sensors_pins)
        self.led = led.Led(led_pins[0], led_pins[1], led_pins[2])

    def play_ringtone(self, volume):
        self.ringtone = pulseaudio.Play(
            [(self.blt_speaker.pa_index, volume)], "axel.mp3")

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

    def __led_standby(self):
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


    def led_standby_on(self):
        led_thread = threading.Thread(target=self.__led_standby)
        sensors_thread = threading.Thread(target=self.sensors.wait_for_movement)
        sensors_thread.start()
        led_thread.start()
        sensors_thread.join()
        self.standby_on = False

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

    chandelier = Chandelier([16, 26], [20, 21, 21],
                            "30:21:A0:29:85:28", "2A:07:98:10:34:2C") #sensors, leds, speaker, remote
    #chandelier.led_standby_on()
    chandelier.led_after_detection()
    sleep(3)
    chandelier.play_ringtone(2)
    sleep(30)
    #chandelier.led_after_detection()
    #chandelier.play_ringtone(1)
    #sleep(50)
    #chandelier.play_voices(1)
    ##chandelier.led_after_detection()
    #sleep(10)
    #chandelier.led_after_pick_up()
    #sleep(10)
    #print("casd")
    #chandelier.led_standby_on()
    #print("cos")
    #sleep(10)
    #chandelier.led_standby_off()
    # chandelier.sensors.wait_for_movement()

