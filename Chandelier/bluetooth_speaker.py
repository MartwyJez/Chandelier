'''
Try to connect to speaker endlessly. If connected return name and index of pulseaudio sink. If errored in bluetooth control module, restart device.
'''
from retry import retry
import subprocess
import sys
from .utilities import *


class DeviceNotFoundError(Exception):
   """Raised when bluetooth adapter can't find device with given address"""
   pass

class BluetoothSpeaker:   
    @retry(DeviceNotFoundError,tries=-1, delay=3)
    def __scan__(self):
        try:
            subprocess.run(["bluetoothctl", "--timeout,", "5", "scan on"]).check_returncode()
            
            devices=subprocess.run(["bluetoothctl", "--timeout,", "5", "devices"])
            devices.check_returncode
            if not devices.stdout.find(self.addr):
                raise DeviceNotFoundError
        except DeviceNotFoundError:
            errprint("Bluetooth couldn't find device. Retrying.")
            subprocess.run(["bluetoothctl", "--timeout,", "5", "scan off"]).check_returncode()
        except subprocess.CalledProcessError:
            errprint("Bluetoothctl have problem with scan or device command. Rebooting")
            sys.exit(10)

    def __init__(self, addr):
        self.addr=addr
        self.__scan__()
