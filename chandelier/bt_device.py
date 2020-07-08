'''
Module for connecting to generic bluetooth device.
'''

from time import sleep
import sys
import pexpect
from retry import retry
from .utilities import errprint, stdprint

class BluetoothDevice:
    """ Class for generic bluetooth. Can be connected, checked if connected and is disconnecting
    when object remove."""
    class BluetoothError(Exception):
        """Raised when bluetooth adapter have problem"""

    class DeviceNotFound(Exception):
        """Raised when given device can't be found"""

    def check_if_connected(self):
        try:
            hci = pexpect.spawn("hcitool con")
            if hci.expect([self.addr, pexpect.EOF]) == 0:
                return True
            else:
                return False
        except pexpect.ExceptionPexpect as exception:
            errprint(exception)
            return False

    def __end_connection__(self):
        self.__interface__.sendline("\ndisconnect")
        self.__interface__.expect("diconnected", timeout=5)


    @retry(pexpect.exceptions.TIMEOUT, tries=20)
    def __check_if_device_is_visible__(self):
        try:
            self.__interface__.sendline("\ndevices")
            self.__interface__.expect(self.addr)
        except self.DeviceNotFound as exception:
            raise exception

    @retry(pexpect.exceptions.TIMEOUT, tries=120)
    def __connect_to_device__(self):
        self.__interface__.sendline("\nconnect "+self.addr)
        self.__interface__.expect("Connection successful", timeout=5)
        while not self.check_if_connected():
            sleep(10)

    def __pair__(self):
        try:
            self.__interface__.sendline("\npaired-devices")
            try:
                self.__interface__.expect(self.addr)
            except pexpect.exceptions.TIMEOUT:
                self.__interface__.sendline("\npair " + self.addr)
                self.__interface__.expect("Pairing successful")
        except:
            raise self.BluetoothError

    def __open_interface__(self):
        try:
            # open bluetoothctl process
            bluetoothctl = pexpect.spawn("bluetoothctl")
            # enable debuging to stdout
            if self.__debug_on__:
                bluetoothctl.logfile = sys.stdout.buffer
            return bluetoothctl
        except Exception as exception:
            errprint(exception)
            errprint("Raspberry have problem with bluetoothctl.")
            raise self.BluetoothError

    def __prepare_bluetooth__(self, __agent__):
        try:
            self.__interface__.sendline("\nagent off")
            self.__interface__.sendline("\nagent " + __agent__)
            self.__interface__.sendline("\ndefault-agent")
            self.__interface__.expect("successful")
            self.__interface__.sendline("\npower on")
            self.__interface__.expect("succeeded")
            self.__interface__.sendline("\npairable on")
            self.__interface__.expect("succeeded")
            self.__interface__.sendline("\nscan on")
            self.__interface__.expect("started")
        except Exception as exception:
            errprint(exception)
            errprint("Raspberry have problem with prepare bluetooth.")
            raise self.BluetoothError

    def __connect__(self):
        try:
            self.__check_if_device_is_visible__()
            stdprint("Device " + self.addr + " is visible")
            self.__pair__()
            stdprint("Device " + self.addr + " is paired")
            self.__connect_to_device__()
            stdprint("Connection to " + self.addr + " are estabilished")
        except self.DeviceNotFound as exception:
            errprint(exception)
            errprint("Rasberry couldn't find device or connect.")
            raise exception
        except self.BluetoothError as exception:
            errprint(exception)
            errprint("Rasberry couldn't pair to the device.")
            raise exception

    def __init__(self, addr, debug=False, agent="NoInputNoOutput"):
        try:
            self.addr = addr
            self.__debug_on__ = debug
            self.__agent__ = agent
            if self.check_if_connected():
                stdprint("Device already connected.")
                return None
            self.__interface__ = self.__open_interface__()
            self.__prepare_bluetooth__(self.__agent__)
            self.__connect__()
            self.__interface__.kill(15)
        except Exception as exception:
            print(exception)
            self.__interface__ = self.__open_interface__()
            #self.__end_connection__()
            raise exception

    #def __del__(self):
    #    self.__interface__ = self.__open_interface__()
    #    try:
    #        #self.__end_connection__()
    #    except:
    #        pass
    #    stdprint("Device " + self.addr + " is disconnected!")
