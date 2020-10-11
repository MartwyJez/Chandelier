from time import sleep
import threading
from retry import retry
from chandelier import bt_devices, led, movement_sensor, pulseaudio

class Chandelier:
    standby_on = True
    playing_voices = False
    press_duration = ""

    @retry(Exception, tries=10, delay=2)
    def connect_to_remote(self, addr):
        remote = bt_devices.BluetoothRemote(addr)
        return remote

    def __init__(self, sensors_pins, led_pins, speaker_addr, remote_addr):
        self.blt_speaker = bt_devices.BluetoothSpeaker(speaker_addr)
        #self.remote = self.connect_to_remote(remote_addr)
        self.sensors = movement_sensor.MovementSensors(sensors_pins)
        self.led = led.Led(led_pins[0], led_pins[1], led_pins[2])

    def play_ringtone(self, volume):
        self.ringtone = pulseaudio.Play(
            [(self.blt_speaker.pa_index, volume)], "../ringtone.mp3")

    def stop_playing_ringtone(self):
        self.ringtone.stop_playing()
        self.ringtone = None

    def play_voices(self, volume=1):
        self.voices_player = pulseaudio.Play(
            [(self.blt_speaker.pa_index, volume)], "../ringtone.mp3", repeat=False)

    def play_failed(self, volume=1):
        self.fail_player = pulseaudio.Play(
            [(self.blt_speaker.pa_index, volume)], "../ringtone.mp3", repeat=False)

    def play_successed(self, volume=1):
        self.success_player = pulseaudio.Play(
            [(self.blt_speaker.pa_index, volume)], "./axel.mp3", repeat=False)

    def stop_playing_voices(self):
        self.voices_player.stop_playing()
        self.voices_player = None

    def stop_led(self):
        self.led.set_r_intensity(0)
        self.led.set_g_intensity(0)

    def led_white(self):
        self.stop_led()
        self.led.set_r_intensity(100)
        self.led.set_g_intensity(100)

    def led_red(self):
        self.stop_led()
        self.led.set_r_intensity(100)
        self.led.set_g_intensity(0)

    def __led_pulsing_white(self):
        self.stop_led()
        while self.standby_on:
            for i in range(1, 155, 1):
                self.led.set_r_intensity(pow(1.03, i))
                self.led.set_g_intensity(pow(1.03, i))
                if not self.standby_on:
                    return True
                sleep(0.03)

            sleep(0.03)

            for i in range(155, 1, -1):
                self.led.set_r_intensity(pow(1.02, i))
                self.led.set_g_intensity(pow(1.02, i))
                if not self.standby_on:
                    return True
                sleep(0.03)

    def led_pulsing_red(self):
        self.stop_led()
        while self.standby_on:
            for i in range(1, 155, 1):
                self.led.set_r_intensity(pow(1.03, i))
                if not self.playing_voices:
                    print("kup")
                    return True
                sleep(0.03)

            sleep(0.03)

            for i in range(155, 1, -1):
                self.led.set_r_intensity(pow(1.02, i))
                if not self.playing_voices:
                    print("kup")
                    return True
                sleep(0.03)

    def wait_between_seq(self):
        ambient = pulseaudio.Play([(self.blt_speaker.pa_index, 1)], "../ringtone.mp3")
        button_thread = threading.Thread(target=self.wait_for_pick_up)
        button_thread.join(175)
        ambient.stop_playing()
        ambient = None

    def wait_for_beggining(self):
        ambient = pulseaudio.Play([(self.blt_speaker.pa_index, 1)], "./axel.mp3")
        led_thread = threading.Thread(target=self.__led_pulsing_white)
        sensors_thread = threading.Thread(
            target=self.sensors.wait_for_movement)
        sensors_thread.start()
        led_thread.start()
        sensors_thread.join()
        self.standby_on = False
        ambient.stop_playing()
        ambient = None

    def voices(self):
        self.playing_voices = True
        led_thread = threading.Thread(target=self.led_pulsing_red)
        button_thread = threading.Thread(target=self.wait_for_pick_up)
        #self.play_voices()
        led_thread.start()
        button_thread.start()
        while button_thread.is_alive():# and self.voices_player.is_playing():
            sleep(0.5)
        #while self.voices_player.is_playing():
        #    sleep(0.5)
        #self.stop_playing_voices()
        self.remote.stop_waiting_on_output()
        self.playing_voices = False
        return self.press_duration

    def fail(self):
        self.led_red()
        self.play_failed()

    def success(self):
        self.led_white()
        self.play_successed()

    def wait_for_pick_up(self):
        butt_down = self.remote.wait_and_get_output()
        if type(butt_down) is None:
            self.press_duration = False
            return False
        elif butt_down.keystate == 1:
            butt_up = self.remote.wait_and_get_output()
            if butt_up.keystate == 0:
                if butt_up.event.sec - butt_down.event.sec >= 3:
                    self.press_duration = "long"
                    return self.press_duration
                else:
                    self.press_duration = "short"
                    return self.press_duration


#2A:07:98:10:34:2C ribbon remote
#2A:07:98:10:32:05 with sticker remote

def main():
    chandelier = Chandelier([16, 19, 26], [20, 21, 21],
                            "0C:A6:94:62:67:40", "2A:07:98:10:32:05")  # sensors, leds, speaker, remote
    chandelier.wait_for_beggining()
    sleep(100)
    chandelier.led_white()
    sleep(2)
    chandelier.play_ringtone(1)
    chandelier.wait_for_pick_up()
    print(1)
    chandelier.stop_playing_ringtone()
    print(2)
    press_duration = chandelier.voices()
    print(press_duration)
    #if press_duration == "long":
    #    chandelier.fail()
    #else:
    #    chandelier.success()
    #chandelier.wait_between_seq()