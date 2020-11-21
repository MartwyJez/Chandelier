from time import sleep
import time
import threading
from sys import exit
from retry import retry
import gc
from chandelier import bt_devices, led, movement_sensor, pulseaudio

global shit_happens
shit_happens = False

class Chandelier:
    standby_on = True
    playing_voices = False
    waiting = False
    press_duration = ""
    leds = False

    @retry(Exception, tries=3, delay=1)
    def connect_to_remote(self):
        self.remote = bt_devices.BluetoothRemote(self.remote_addr)

    def __init__(self, sensors_pins, led_pins, speaker_addr, remote_addr):
        self.remote_addr = remote_addr
        self.connect_to_remote()
        self.blt_speaker = bt_devices.BluetoothSpeaker(speaker_addr, disconnect=False)
        self.pa = pulseaudio.OutputControl([0, self.blt_speaker.pa_index])
        self.sensors = movement_sensor.MovementSensors(sensors_pins)
        self.led = led.Led(led_pins[0], led_pins[1], led_pins[2])
        global shit_happens
        if shit_happens:
            print("Shit happened when trying to connect to bluetooth device!")
            exit("14")

    def play_ringtone(self, volume):
        self.ringtone = pulseaudio.Play(
            [(self.blt_speaker.pa_index, volume)], "../ringtone.mp3", self.pa)

    def stop_playing_ringtone(self):
        self.ringtone.stop_playing()
        self.ringtone = None

    def play_voices(self, volume=3):
        self.voices_player = pulseaudio.Play(
            [(0, volume)], "/home/pi/NAGRANIE_FINAL_BASIC.wav", self.pa, repeat=False)

    def play_failed(self, volume=2):
        self.fail_player = pulseaudio.Play(
            [(self.blt_speaker.pa_index, volume)], "./lose.wav", self.pa, repeat=False)
        while not self.fail_player.is_playing():
            sleep(0.1)
        while self.fail_player.is_playing():
            sleep(0.5)
        self.fail_player.stop_playing()
        self.fail_player = None

    def play_successed(self, volume=2):
        self.success_player = pulseaudio.Play(
            [(self.blt_speaker.pa_index, volume)], "./win.wav", self.pa, repeat=False)
        while not self.success_player.is_playing():
            sleep(0.1)
        while self.success_player.is_playing():
            sleep(0.5)
        self.success_player.stop_playing()
        self.success_player = None

    def stop_playing_voices(self):
        self.voices_player.stop_playing()
        self.voices_player = None

    def stop_led(self):
        self.led.set_r_intensity(0)
        self.led.set_g_intensity(0)

    def led_white(self):
        while self.leds:
            for i in range(140, 186, 1):
                self.led.set_r_intensity(pow(1.025, i))
                self.led.set_g_intensity(pow(1.025, i))
                if self.leds:
                    return True
                sleep(0.03)

            sleep(0.03)

            for i in range(186, 140, -1):
                self.led.set_r_intensity(pow(1.025, i))
                self.led.set_g_intensity(pow(1.025, i))
                if self.leds:
                    return True
                sleep(0.03)


    def led_red(self):
        while self.leds:
            for i in range(140, 186, 1):
                self.led.set_r_intensity(pow(1.025, i))
                self.led.set_g_intensity(0)
                if self.leds:
                    return True
                sleep(0.03)

            sleep(0.03)

            for i in range(186, 140, -1):
                self.led.set_r_intensity(pow(1.025, i))
                self.led.set_g_intensity(0)
                if self.leds:
                    return True
                sleep(0.03)

    def __led_pulsing_white(self):
        while self.standby_on:
            for i in range(1, 35, 1):
                self.led.set_r_intensity(pow(1.035, i))
                self.led.set_g_intensity(pow(1.035, i))
                if not self.standby_on:
                    return True
                sleep(0.03)
            for i in range(35, 186, 1):
                self.led.set_r_intensity(pow(1.025, i))
                self.led.set_g_intensity(pow(1.025, i))
                if not self.standby_on:
                    return True
                sleep(0.03)

            sleep(0.03)

            for i in range(186, 35, -1):
                self.led.set_r_intensity(pow(1.025, i))
                self.led.set_g_intensity(pow(1.025, i))
                if not self.standby_on:
                    return True
                sleep(0.03)
            for i in range(35, 1, -1):
                self.led.set_r_intensity(pow(1.035, i))
                self.led.set_g_intensity(pow(1.035, i))
                if not self.standby_on:
                    return True
                sleep(0.03)

    def led_pulsing_red(self):
        while self.playing_voices:
            for i in range(1, 35, 1):
                self.led.set_r_intensity(pow(1.035, i))
                self.led.set_g_intensity(0)
                if not self.playing_voices:
                    return True
                sleep(0.03)
            for i in range(35, 186, 1):
                self.led.set_r_intensity(pow(1.025, i))
                self.led.set_g_intensity(0)
                if not self.playing_voices:
                    return True
                sleep(0.03)

            sleep(0.03)

            for i in range(186, 35, -1):
                self.led.set_r_intensity(pow(1.025, i))
                if not self.playing_voices:
                    return True
                sleep(0.03)
            for i in range(35, 1, -1):
                self.led.set_r_intensity(pow(1.035, i))
                if not self.playing_voices:
                    return True
                sleep(0.03)
    def ambient_play(self):
        self.ambient_player = pulseaudio.Play([(self.blt_speaker.pa_index, 2)], "/home/pi/ambient1.wav", self.pa)
    
    def ambient_stop_play(self):
        self.ambient_player.stop_playing()
        self.ambient_player = None

    def wait_between_seq(self):
        self.waiting = True
        led_thread = threading.Thread(target=self.__led_pulsing_white, daemon=True)
        self.ambient_play()
        button_thread = threading.Thread(target=self.wait_for_pick_up)
        button_thread.start()
        led_thread.start()
        button_thread.join(999)
        self.stop_led()
        sleep(0.3)
        self.leds=True
        self.led_white()
        sleep(0.3)
        self.leds=False
        self.stop_led()
        sleep(0.3)
        self.leds=True
        self.led_white()
        sleep(0.3)
        self.leds=False
        self.stop_led()
        sleep(0.3)
        self.leds=True
        self.led_white()
        sleep(0.3)
        self.leds=False
        self.ambient_stop_play()

    def wait_for_beggining(self):
        self.ambient_play()
        led_thread = threading.Thread(target=self.__led_pulsing_white)
        sensors_thread = threading.Thread(
            target=self.sensors.wait_for_movement)
        sensors_thread.start()
        led_thread.start()
        sleep(10)
        sensors_thread.join()
        self.standby_on = False
        self.ambient_stop_play()

    def voices(self):
        self.press_duration = ""
        self.playing_voices = True
        led_thread = threading.Thread(target=self.led_pulsing_red)
        button_thread = threading.Thread(target=self.wait_for_pick_up)
        led_thread.start()
        sleep(1)
        self.play_voices()
        while not self.voices_player.is_playing():
            sleep(0.1)
        button_thread.start()
        while (self.press_duration == "" or self.press_duration == "short") and self.voices_player.is_playing():
            sleep(0.25)
        self.stop_playing_voices()
        if self.press_duration == "":
            self.remote.stop_waiting_on_output()
        self.playing_voices = False
        return self.press_duration

    def fail(self):
        self.leds = True
        threading.Thread(target=self.led_red, daemon=True)
        self.play_failed()
        self.leds = False

    def success(self):
        self.leds = True
        threading.Thread(target=self.led_white, daemon=True)
        self.play_successed()
        self.leds = False

    def wait_for_pick_up(self):
        print("imin")
        start = time.time()
        time.clock()
        elapsed = 0
        while True:
            elapsed = time.time() - start
            if elapsed and self.waiting > 10:
                threading.Thread(target=self.connect_to_remote, daemon=True).start()
            butt_down = self.remote.wait_and_get_output()
            if type(butt_down) == None:
                self.press_duration = ""
                return False
            elif butt_down.keystate == 1:
                butt_up = self.remote.wait_and_get_output()
                if butt_up.keystate == 0:
                    if butt_up.event.sec - butt_down.event.sec >= 3:
                        print("long")
                        self.press_duration = "long"
                        return self.press_duration
                    else:
                        self.press_duration = "short"
                        print("short")
                        if not self.waiting and not self.playing_voices:
                          return self.press_duration

def sequence():
    chandelier = Chandelier([26, 19, 16], [20, 21, 21],
                        "0C:A6:94:62:67:40", "2A:07:98:10:32:05")  # sensors, leds, speaker, remote
    chandelier.wait_for_beggining()
    chandelier.leds = True
    threading.Thread(target=chandelier.led_white, daemon=True)
    chandelier.play_ringtone(1)
    chandelier.wait_for_pick_up()
    chandelier.leds = False
    chandelier.stop_playing_ringtone()
    press_duration = chandelier.voices()
    if press_duration == "long":
        chandelier.fail()
    else:
        chandelier.success()

def waiting():
    chandelier = Chandelier([26, 19, 16], [20, 21, 21],
                    "0C:A6:94:62:67:40", "2A:07:98:10:32:05")  # sensors, leds, speaker, remote
    chandelier.wait_between_seq()

#2A:07:98:10:34:2C ribbon remote
#2A:07:98:10:32:05 with sticker remote

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Seq or waiting')
    parser.add_argument('--wait', action='store_true', help='Execute waiting sequence')
    args = parser.parse_args()

    if args.wait:
        waiting()
    else:
        sequence()

