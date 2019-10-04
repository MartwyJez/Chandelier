from . import *
import threading
import sys
from time import sleep


def ConnectToSpeaker(addr,retry=10,debug=False):
    for i in range(1, retry):
        try:
            return bluetooth_speaker.BluetoothSpeaker(addr,debug=debug)
        except bluetooth_speaker.BluetoothSpeaker.DeviceNotFound:
            continue
        except Exception:
            sys.exit(10)

def ThreadCheckIfConnect(blt_speaker):
    while blt_speaker.CheckIfConnected():
        sleep(10)
    utilities.errprint("Device lost connection, program will exit.")
    sys.exit(11)

def main():
    blt_speaker = ConnectToSpeaker("0C:A6:94:62:67:40",debug=False)
    threading.Thread(target=ThreadCheckIfConnect, args=(blt_speaker,)).start()
    #pulseaudio.Play(,"/home/pi/axel.mp3")
    pulseaudio.Play([(blt_speaker.paindex,1.0)],"axel.mp3")
    #initialize leds
    #if ruch then ring and white leds
    #if pushed buttons then voices and red leds
    # sleep for two minutes
