'''
Try to connect to speaker endlessly. If connected return name and index of pulseaudio sink. If errored in bluetooth control module, restart device.
'''
from retry import retry
import pexpect
import time
import io
from .utilities import *


class BluetoothError(Exception):
    """Raised when bluetooth adapter have problem"""
    pass


class BluetoothDevice:
    def __end_connection__(self):
        if self.interface:
            self.interface.sendline("\ndisconnect")
            self.interface.sendline("\nscan off")
            if not self.interface.terminate():
                self.interface.terminate(force=True)
    
    @retry(pexpect.exceptions.TIMEOUT, tries=20)
    def __check_if_device_is_visible__(self):
        self.interface.sendline("\ndevices")
        self.interface.expect(self.addr)

    def __pair__(self):
        self.interface.sendline("\npaired-devices")
        try:
            self.interface.expect(self.addr)
        except pexpect.exceptions.TIMEOUT:
            self.interface.sendline("\npair " + self.addr)
            self.interface.expect("Pairing successful")

    def __open_interface__(self):
        try:
            # open bluetoothctl process
            bluetoothctl = pexpect.spawn("bluetoothctl")
            # enable debuging to stdout
            if self.DEBUG:
                bluetoothctl.logfile = sys.stdout.buffer
            return bluetoothctl
        except Exception as e:
            errprint(e)
            errprint(
                "Raspberry have problem with bluetoothctl.")
            raise BluetoothError

    def __prepare_bluetooth__(self, agent):
        try:
            self.interface.sendline("\nagent off")
            self.interface.sendline("\nagent " + agent)
            self.interface.sendline("\ndefault-agent")
            self.interface.expect("successful")
            self.interface.sendline("\npower on")
            self.interface.expect("succeeded")
            self.interface.sendline("\npairable on")
            self.interface.expect("succeeded")
            self.interface.sendline("\nscan on")
            self.interface.expect("started")
        except Exception as e:
            errprint(e)
            errprint("Raspberry have problem with prepare bluetooth.")
            raise BluetoothError

    def __connect__(self):
        try:
            self.__check_if_device_is_visible__()
            stdprint("Device " + self.addr + " was found")
            self.__pair__()
            stdprint("Device " + self.addr + " is paired")

            self.interface.sendline("\nconnect "+self.addr)
            self.interface.expect("Connection successful")
            stdprint("Connection to " + self.addr + " are estabilished")
        except Exception as e:
            errprint(e)
            errprint("Rasberry couldn't find, pair or connect to the device.")
            raise BluetoothError

    def __init__(self, addr, debug=False, agent="NoInputNoOutput"):
        try:
            self.addr = addr
            self.DEBUG = debug
            self.agent = agent
            self.interface = self.__open_interface__()
            self.__prepare_bluetooth__(self.agent)
            self.__connect__()
        except Exception as e:
            self.__end_connection__()
            sys.exit(10)

    def __del__(self):
        self.__end_connection__()
