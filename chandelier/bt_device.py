'''
Module for connecting to generic bluetooth device.
'''

from time import sleep
import sys
import re
import pexpect
from retry import retry
from .utilities import errprint, stdprint

def reset_config():
    try:
        hci_name = re.search('hc..', pexpect.spawn('hcitool dev').read().decode("utf-8")).group(0)
        hci = pexpect.spawn("sudo hciconfig "+ hci_name +" reset")
        if hci.expect(pexpect.EOF) == 0:
            return True
        else:
            return False
    except pexpect.ExceptionPexpect as exception:
        errprint(exception)
        return False

class BluetoothDevice:
    """ Class for generic bluetooth. Can be connected, checked if connected and is disconnecting
    when object remove."""
    class BluetoothError(Exception):
        """Raised when bluetooth adapter have problem"""

    class DeviceNotFound(Exception):
        """Raised when given device can't be found"""

    def is_connected(self):
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
        if not hasattr(self, '__interface__'):
            self.__interface__ = self.__open_interface__()
            self.__prepare_bluetooth__(self.__agent__)
        print("Disconnecting!")
        self.__interface__.sendline("\ndisconnect " + self.addr)
        self.__interface__.expect("Successful disconnected", timeout=5)
        self.__interface__.sendline("\nremove " + self.addr)
        self.__interface__.expect("Device has been removed", timeout=5)
        self.__interface__.close(force=True)
        sleep(5)

    @retry(pexpect.exceptions.TIMEOUT, tries=3, delay=1)
    def __is_device_visible__(self):
        try:
            self.__interface__.sendline("\ndevices")
            self.__interface__.expect(self.addr, timeout=5)
        except self.DeviceNotFound as exception:
            raise exception

    @retry(pexpect.exceptions.TIMEOUT, tries=3, delay=2)
    def __connect_to_device__(self):
        self.__interface__.sendline("\nconnect "+self.addr)
        self.__interface__.expect("Connection successful", timeout=5)
        sleep(2)
        if not self.is_connected():
            raise pexpect.exceptions.TIMEOUT

    def __trust__(self):
        self.__interface__.sendline("\ntrust " + self.addr)
        self.__interface__.expect("trust succeeded", timeout=5)

    def __pair__(self):
        try:
            self.__interface__.sendline("\npaired-devices")
            try:
                self.__interface__.expect(self.addr, timeout=5)
            except pexpect.exceptions.TIMEOUT:
                self.__interface__.sendline("\npair " + self.addr)
                self.__interface__.expect("Pairing successful", timeout=5)
        except:
            raise self.BluetoothError

    def __open_interface__(self):
        try:
            # open bluetoothctl process
            bluetoothctl = pexpect.spawn("bluetoothctl")
            # enable debuging to stdout
            if self.__debug_on__:
                bluetoothctl.logfile = sys.stdout.buffer
            sleep(3)
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
            self.__interface__.expect("successful", timeout=5)
            self.__interface__.sendline("\npower on")
            self.__interface__.expect("succeeded", timeout=5)
            self.__interface__.sendline("\npairable on")
            self.__interface__.expect("succeeded", timeout=5)
            self.__interface__.sendline("\nscan on")
            self.__interface__.expect("started", timeout=5)
        except Exception as exception:
            errprint(exception)
            errprint("Raspberry have problem with prepare bluetooth.")
            raise self.BluetoothError

    def __connect__(self):
        try:
            self.__is_device_visible__()
            stdprint("Device " + self.addr + " is visible")
            sleep(1)
            self.__trust__()
            self.__pair__()
            sleep(1)
            stdprint("Device " + self.addr + " is paired")
            self.__connect_to_device__()
            sleep(1)
            stdprint("Connection to " + self.addr + " is estabilished")
        except self.DeviceNotFound as exception:
            errprint(exception)
            errprint("Rasberry couldn't find device or connect.")
            raise exception
        except self.BluetoothError as exception:
            errprint(exception)
            errprint("Rasberry couldn't pair to the device.")
            raise exception

    def __init__(self, addr, disconnect=True, debug=False, agent="NoInputNoOutput"):
        try:
            self.disconnect_on_failure = disconnect
            self.addr = addr
            self.__debug_on__ = debug
            self.__agent__ = agent
            if self.is_connected():
                stdprint("Device already connected.")
                return None
            self.__interface__ = self.__open_interface__()
            self.__prepare_bluetooth__(self.__agent__)
            self.__connect__()
            self.__interface__.close(force=True)
            print("Interface is killed")
        except Exception as exception:
            global shit_happens
            print(exception)
            if self.disconnect_on_failure:
                reset_config()
                self.__interface__ = self.__open_interface__()
                self.__end_connection__()
                self.__interface__.close(force=True)
            shit_happens = True
            print("Interface is killed")
            raise exception

    #def __del__(self):
    #    if self.__debug_on__:
    #        print("disconnect")
    #        self.__interface__ = self.__open_interface__()
    #        try:
    #            self.__end_connection__()
    #        except:
    #            pass
    #        stdprint("Device " + self.addr + " is disconnected!")
