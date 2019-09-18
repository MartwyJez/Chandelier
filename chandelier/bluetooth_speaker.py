'''
Try to connect to speaker endlessly. If connected return name and index of pulseaudio sink. If errored in bluetooth control module, restart device.
'''
from __future__ import print_function
import subprocess
from retry import retry

class DeviceNotFoundError(Exception):
   """Raised when bluetooth adapter can't find device with given address"""
   pass

class BluetoothSpeaker:   
    @retry(exception=DeviceNotFoundError,tries=-1, delay=3)
    def __scan__(self):
        try:
            subprocess.run(["bluetoothctl", "--timeout,", "5", "scan on"]).check_returncode()
            
            devices=subprocess.run(["bluetoothctl", "--timeout,", "5", "devices"])
            devices.check_returncode
            if not devices.stdout.find(self.addr):
                raise DeviceNotFoundError
        except DeviceNotFoundError:
            subprocess.run(["bluetoothctl", "--timeout,", "5", "scan off"]).check_returncode()
        except CalledProcessError:
            eprint("Bluetoothctl have problem with scan or device command. Rebooting")
            sys.exit(1)

    def __init__(self, addr):
        self.addr=addr
        self.__scan__()
