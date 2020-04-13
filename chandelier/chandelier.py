import threading
import sys
from time import sleep
from . import bt_devices, led, movement_sensor, pulseaudio
from .utilities import errprint
import asyncio

def connect_to_speaker(addr, retry=10, debug=False):
    for i in range(1, retry):
        try:
            return bt_devices.BluetoothSpeaker(addr, debug=debug)
        except bt_devices.BluetoothSpeaker.DeviceNotFound:
            continue
        except Exception as exception:
            errprint('An exception occurred: %r', exception)
            sys.exit(10)


def scarry_voices():
    pulseaudio.Play([(0, 1.0)], "../ambient1.wav")

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

#def WaitForRemoteInput():
#    remote = bt_devices.BluetoothRemote("2A:07:98:10:32:05")
#    remote.WaitForOutput()

async def listen_for_movement(sensor):
    sensor.wait_for_movement()

def sequence():
    pulseaudio.Play([(blt_speaker.paindex, 1.0)], "axel.mp3")

def main():
    #blt_speaker = connect_to_speaker("0C:A6:94:62:67:40", debug=False)
    blt_speaker = connect_to_speaker("18:1D:EA:A0:2F:D4", debug=False)
    remote = bt_devices.BluetoothRemote("2A:07:98:10:34:2C")
    sensors_pins = [19]
    sensors = []
    for pin in sensors_pins:
        sensors.append(movement_sensor(pin))

    tasks = []
    for sensor in sensors:
        tasks.append(asyncio.create_task(listen_for_movement(sensor)))

    await asyncio.gather(tasks)

    ##threading.Thread(target=Chandelier, args=(blt_speaker), daemon=True).start()
    #threading.Thread(target=scarry_voices, args=(), daemon=True).start()
    #
    #blt_speaker = "1"
    #if manage_buttons(remote) == "long":
    #    scarry_thr = threading.Thread(target=scarry_voices, args=())
    #    scarry_thr.start()
    #    scarry_thr.join()
    #else:
    #    ringtone_thr = threading.Thread(target=ringtone, args=(blt_speaker))
    #    ringtone_thr.start()
    #    while ringtone_thr.is_alive():
    #        if manage_buttons(remote) == "long":
    #            scarry_thr = threading.Thread(target=scarry_voices, args=())
    #            scarry_thr.start()
    #            scarry_thr.join()


    #sleep(50)

    #while blt_speaker.CheckIfConnected():
    #    sleep(10)
    #utilities.errprint("Device lost connection, program will exit.")

    #initialize leds
    #if ruch then ring and white leds
    #if pushed buttons then voices and red leds
    # sleep for two minutes
