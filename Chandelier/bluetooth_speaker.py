'''
Try to connect to speaker endlessly. If connected return name and index of pulseaudio sink. If errored in bluetooth control module, restart device.
'''
from retry import retry
import pexpect
import time
import io
import pulsectl
from .utilities import *


class BluetoothError(Exception):
    """Raised when bluetooth adapter have problem"""
    pass

class BluetoothDevice:
    def __end_connection__(self):
        if self.__interface__:
            self.__interface__.sendline("\ndisconnect")
            self.__interface__.sendline("\nscan off")
            if not self.__interface__.terminate():
                self.__interface__.terminate(force=True)

    @retry(pexpect.exceptions.TIMEOUT, tries=20)
    def __check_if_device_is_visible__(self):
        self.__interface__.sendline("\ndevices")
        self.__interface__.expect(self.addr)

    def __pair__(self):
        self.__interface__.sendline("\npaired-devices")
        try:
            self.__interface__.expect(self.addr)
        except pexpect.exceptions.TIMEOUT:
            self.__interface__.sendline("\npair " + self.addr)
            self.__interface__.expect("Pairing successful")

    def __open_interface__(self):
        try:
            # open bluetoothctl process
            bluetoothctl = pexpect.spawn("bluetoothctl")
            # enable debuging to stdout
            if self.__DEBUG__:
                bluetoothctl.logfile = sys.stdout.buffer
            return bluetoothctl
        except Exception as e:
            errprint(e)
            errprint(
                "Raspberry have problem with bluetoothctl.")
            raise BluetoothError

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

            self.__interface__.sendline("\nconnect "+self.addr)
            self.__interface__.expect("Connection successful")
            stdprint("Connection to " + self.addr + " are estabilished")
        except Exception as e:
            errprint(e)
            errprint("Rasberry couldn't find, pair or connect to the device.")
            raise BluetoothError

    def __init__(self, addr, debug, agent):
        try:
            self.addr = addr
            self.__DEBUG__ = debug
            self.__agent__ = agent
            self.__interface__ = self.__open_interface__()
            self.__prepare_bluetooth__(self.__agent__)
            self.__connect__()
        except Exception:
            self.__end_connection__()
            sys.exit(10)

    def __del__(self):
        self.__end_connection__()

class BluetoothSpeaker(BluetoothDevice):
    def __GetPulseAudioSink__(self):
        with pulsectl.Pulse('list-sinks') as pulse:
            for sink in pulse.sink_list():
                if sink.proplist.get('device.string')==self.addr:
                    return sink.index, sink.name


    def __init__(self, addr, debug=False, agent="NoInputNoOutput"):
        super().__init__(self, addr, debug, agent)
        self.paindex, self.paname = self.__GetPulseAudioSink__()
        
