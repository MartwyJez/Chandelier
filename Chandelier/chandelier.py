from . import *
import threading
import sys
from time import sleep


def ConnectToSpeaker(addr,retry=10,debug=False):
    for i in range(1, retry):
        try:
            return bt_devices.BluetoothSpeaker(addr,debug=debug)
        except bt_devices.BluetoothSpeaker.DeviceNotFound:
            continue
        except Exception:
            sys.exit(10)

def Ringtone(blt_speaker):
    #pulseaudio.Play([(blt_speaker.paindex,1.0)],"axel.mp3")
    pulseaudio.Play([(0,1.4)],"axel.mp3")

def ScarryVoices():
    pulseaudio.Play([(0,1.4)],"../ambient1.wav")

def ManageButtons(remote):
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

def main():
    #blt_speaker = ConnectToSpeaker("0C:A6:94:62:67:40",debug=False)
    #threading.Thread(target=Chandelier, args=(blt_speaker), daemon=True).start()
    #threading.Thread(target=ScarryVoices, args=(), daemon=True).start()
    remote = bt_devices.BluetoothRemote("2A:07:98:10:34:2C")
    blt_speaker = "1"
    
    if ManageButtons(remote) == "long":
        scarry_thr = threading.Thread(target=ScarryVoices, args=())
        scarry_thr.start()
        scarry_thr.join()
    else:
        ringtone_thr = threading.Thread(target=Ringtone, args=(blt_speaker))
        ringtone_thr.start()
        while ringtone_thr.is_alive():
            if ManageButtons(remote) == "long": 
                ringtone_thr.
                scarry_thr = threading.Thread(target=ScarryVoices, args=())
                scarry_thr.start()
                scarry_thr.join()


    #sleep(50)

    #while blt_speaker.CheckIfConnected():
    #    sleep(10)
    #utilities.errprint("Device lost connection, program will exit.")
    
    #initialize leds
    #if ruch then ring and white leds
    #if pushed buttons then voices and red leds
    # sleep for two minutes
