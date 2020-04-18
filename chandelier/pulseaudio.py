import pulsectl
import vlc
from time import sleep

class OutputControl():

    def SetVolumeSink(self, Sink):
        temp_vol = Sink[0]().volume
        temp_vol.value_flat = Sink[1]
        self.__interface__.sink_volume_set(Sink[0]().index, temp_vol)

    def __CreateCombinedSink__(self, sinks_list):
        sinks_names = ','.join(Sink[0]().name for Sink in sinks_list)
        print(sinks_names)
        args = "sink_name=HubertPierdoliGlupoty slaves=\"" + \
            sinks_names + "\" sink_properties=\"\""
        sink_module = self.__interface__.module_load("module-combine-sink", args)
        for Sink in self.__interface__.sink_list():
            if Sink.owner_module == sink_module:
                return (lambda: self.__interface__.sink_info(Sink.index), 1.0)

    def __SetDefaultOutput__(self, Sink):
        self.__interface__.sink_default_set(Sink[0]())

    def __init__(self, sinks_index_and_volume):
        self.__interface__ = pulsectl.Pulse('interface')

        self.sinks_list = []
        for Sink in sinks_index_and_volume:
            def sink_pulseaudio(index): return lambda: self.__interface__.sink_info(index)
            self.sinks_list.append((sink_pulseaudio(Sink[0]), float(Sink[1])))

        if len(self.sinks_list) > 1:
            self.sinks_list.insert(0, self.__CreateCombinedSink__(self.sinks_list))
            self.__SetDefaultOutput__(self.sinks_list[0])
            for Sink in self.sinks_list:
                self.SetVolumeSink(Sink)
        else:
            self.__SetDefaultOutput__(self.sinks_list[0])
            self.SetVolumeSink(self.sinks_list[0])


class Play(OutputControl):

    def play(self):
        self.player.play()

    def stop_playing(self):
        self.player.stop()

    def __del__(self):
        self.player.stop()
        self.player.release()

    def __init__(self, sinks, file):
        self.file = file
        self.player = vlc.MediaPlayer(vlc.Instance('--input-repeat=999999'), file)
        super().__init__(sinks)
        self.play()
