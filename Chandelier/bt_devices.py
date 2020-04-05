import evdev
import asyncio
from sys import stdout
from time import sleep
from retry import retry
from . import bt_device, utilities

class BluetoothSpeaker(bt_device.BluetoothDevice):
    
    @retry(Exception, tries=5, delay=3)
    def __GetPulseAudioSink__(self):
        with pulsectl.Pulse('list-sinks') as pulse:
            for sink in pulse.sink_list():
                if sink.proplist.get('device.string') == self.addr:
                    return sink.index, sink.name

    def __init__(self, addr, debug=False, agent="NoInputNoOutput"):
        try:
            super().__init__(addr, debug, agent)
            self.paindex, self.paname = self.__GetPulseAudioSink__()
        except Exception as e:
            utilities.errprint(e)
            raise e


class BluetoothRemote(bt_device.BluetoothDevice):
    remote_inputs=[]
    output = ""
    @retry(Exception, tries=5, delay=3)
    def __RemoteDevices__(self, addr):
        remote_address = addr
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if device.phys not in remote_address:
                devices.remove(device)
        return devices

    def WaitAndGetOutput(self):
        inputs = self.remote_inputs
        async def print_events(device):
            async for event in device.async_read_loop():
                cat_event = evdev.categorize(event)
                if type(cat_event) == evdev.KeyEvent:
                    return cat_event
                
        devs_future = ""
        for device in inputs:
            devs_future = asyncio.ensure_future(print_events(device))

        loop = asyncio.get_event_loop()
        return loop.run_until_complete(devs_future)

    def __init__(self, addr, debug=False, agent="NoInputNoOutput"):
        try:
            super().__init__(addr, debug, agent)
            self.remote_inputs = self.__RemoteDevices__(addr)
        except Exception as e:
            utilities.errprint(e)
            raise e