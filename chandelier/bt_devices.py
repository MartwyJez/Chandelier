import asyncio
from retry import retry
from time import sleep
import evdev
import pulsectl
from . import bt_device, utilities

class BluetoothSpeaker(bt_device.BluetoothDevice):

    @retry(Exception, tries=20, delay=3)
    def __get_pulse_audio_sink__(self):
        with pulsectl.Pulse('list-sinks') as pulse:
            for sink in pulse.sink_list():
                if sink.proplist.get('device.string') == self.addr:
                    return sink.index, sink.name

    def __init__(self, addr, debug=False, agent="NoInputNoOutput"):
        super().__init__(addr, debug, agent)
        sleep(3)
        try:
            self.pa_index, self.paname = self.__get_pulse_audio_sink__()
        except TypeError:
            utilities.errprint("Device " + self.addr + " is not recongized as bluetooth speaker.")
            raise self.BluetoothError



class BluetoothRemote(bt_device.BluetoothDevice):
    __loop = ""
    remote_inputs = []
    output = ""

    def __remote_devices__(self, addr):
        remote_address = addr
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if device.phys == '':
                devices.remove(device)
        if len(devices) == 0:
            raise Exception
        return devices

    def stop_waiting_on_output(self):
        self.__loop.stop()

    def wait_and_get_output(self):
        @asyncio.coroutine
        async def print_events(device):
            async for event in device.async_read_loop():
                cat_event = evdev.categorize(event)
                if isinstance(cat_event, evdev.KeyEvent):
                    asyncio.get_running_loop().stop()
                    return cat_event

        self.__loop = asyncio.new_event_loop()

        tasks = []
        for device in self.remote_inputs:
            tasks.append(self.__loop.create_task(print_events(device)))

        self.__loop.run_forever()

        for task in tasks:
            if task.done():
              return task.result()

    def __init__(self, addr, debug=False, agent="NoInputNoOutput"):
        try:
            super().__init__(addr, debug, agent)
            self.remote_inputs = self.__remote_devices__(addr)
        except Exception as exception:
            utilities.errprint(exception)
            raise exception
