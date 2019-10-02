import pulsectl
from pydub import AudioSegment
from pydub.playback import play


class OutputControl():

    def SetVolumeSink(self, Sink):
        temp_vol = Sink[0]().volume
        temp_vol.value_flat = Sink[1]
        self.__interface__.sink_volume_set(Sink[0]().index, temp_vol)

    def __CreateCombinedSink__(self, sinks_list):
        sinks_names = ', '.join(Sink[0]().name for Sink in sinks_list)
        sinks_indexes = ','.join(Sink[0]().index for Sink in sinks_list)
        args = "sink_name=" + sinks_indexes + "slaves=" + \
            sinks_names + "sink_properties=\"\""
        sink_module = pulse.module_load("module-combine-sink", args)
        for Sink in pulse.sink_list():
            if Sink.owner_module == sink_module:
                return (lambda: self.__interface__.sink_info(Sink.index), 1, 0)

    def __SetDefaultOutput__(self, Sink):
        self.__interface__.sink_default_set(Sink[0]())

    def __init__(self, sinks_index_and_volume):
        self.__interface__ = pulsectl.Pulse('interface')

        self.sinks_list = []
        for Sink in sinks_index_and_volume:
            self.sinks_list.append(
                (lambda: self.__interface__.sink_info(Sink[0]), float(Sink[1])))

        if len(self.sinks_list) > 1:
            self.__SetDefaultOutput__(
                self.__CreateCombinedSink__(self.sinks_list))
            for Sink in self.sinks_list:
                self.SetVolumeSink(Sink)
        else:
            self.__SetDefaultOutput__(self.sinks_list[0])
            self.SetVolumeSink(self.sinks_list[0])


class Play(OutputControl):

    def PlayFile(self, file):
        sound = AudioSegment.from_file(file[0], file[1])
        play(sound)

    def __init__(self, sinks, file):
        self.file = file
        super().__init__(sinks)
        self.PlayFile(self.file)
