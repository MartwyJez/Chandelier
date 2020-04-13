import asyncio
from retry import retry
import evdev
import pulsectl
from . import bt_device, utilities

class BluetoothSpeaker(bt_device.BluetoothDevice):

    @retry(Exception, tries=5, delay=3)
    def __get_pulse_audio_sink__(self):
        with pulsectl.Pulse('list-sinks') as pulse:
            for sink in pulse.sink_list():
                if sink.proplist.get('device.string') == self.addr:
                    return sink.index, sink.name

    def __init__(self, addr, debug=False, agent="NoInputNoOutput"):
        try:
            super().__init__(addr, debug, agent)
            self.paindex, self.paname = self.__get_pulse_audio_sink__()
        except Exception as exception:
            utilities.errprint(exception)
            raise exception


class BluetoothRemote(bt_device.BluetoothDevice):
    remote_inputs = []
    output = ""
    @retry(Exception, tries=5, delay=3)
    def __remote_devices__(self, addr):
        remote_address = addr
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if device.phys not in remote_address:
                devices.remove(device)
        return devices

    def wait_and_get_output(self):
        inputs = self.remote_inputs
        async def print_events(device):
            async for event in device.async_read_loop():
                cat_event = evdev.categorize(event)
                if isinstance(cat_event, evdev.KeyEvent):
                    return cat_event

        devs_future = ""
        for device in inputs:
            devs_future = asyncio.ensure_future(print_events(device))

        loop = asyncio.get_event_loop()
        return loop.run_until_complete(devs_future)

    def __init__(self, addr, debug=False, agent="NoInputNoOutput"):
        try:
            super().__init__(addr, debug, agent)
            self.remote_inputs = self.__remote_devices__(addr)
        except Exception as exception:
            utilities.errprint(exception)
            raise exception
