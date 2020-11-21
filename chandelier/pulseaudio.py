import pulsectl
import vlc

class OutputControl():

    def SetVolumeSink(self, Sink):
        for sink in self.sinks_list:
            if sink().index == Sink[0]:
                temp_vol = sink().volume
                temp_vol.value_flat = Sink[1]
                self.__interface__.sink_volume_set(sink().index, temp_vol)
                return None


    def CreateCombinedSink(self, sinks_list):
        sinks_names = ','.join(Sink().name for Sink in sinks_list)
        print(sinks_names)
        args = "sink_name=HubertPierdoliGlupoty slaves=\"" + \
            sinks_names + "\" sink_properties=\"\""
        sink_module = self.__interface__.module_load("module-combine-sink", args)
        for Sink in self.__interface__.sink_list():
            if Sink.owner_module == sink_module:
                sinks_list.append(lambda: self.__interface__.sink_info(Sink.index))

    def SetDefaultOutput(self, Sink):
        for sink in self.sinks_list:
            if sink().index == Sink:
                self.__interface__.sink_default_set(sink())
                return None

    def __init__(self, sinks_indexes):
        self.__interface__ = pulsectl.Pulse('interface')

        self.sinks_list = []
        for Sink in sinks_indexes:
            def sink_pulseaudio(index): return lambda: self.__interface__.sink_info(index)
            self.sinks_list.append(sink_pulseaudio(Sink))

    def __del__(self):
        self.__interface__.disconnect()
        self.__interface__.close()


class Play():

    def play(self):
        self.player.play()

    def stop_playing(self):
        self.player.stop()
    
    def is_playing(self):
        return self.player.is_playing()

    def __del__(self):
        self.player.stop()
        self.player.release()
        print("player is released!")

    def __init__(self, sinks, file, pa, repeat=True):
        self.file = file
        if len(sinks) > 1:
            pa.__CreateCombinedSink__([item[0] for item in sinks])
            pa.SetDefaultOutput(pa.sinks_list[-1])
        else:
            pa.SetDefaultOutput(sinks[0][0])
        
        for sink in sinks:
            pa.SetVolumeSink(sink)
        
        if repeat:
            self.player = vlc.MediaPlayer(vlc.Instance('--input-repeat=999999'), file)
        else:
            self.player = vlc.MediaPlayer(vlc.Instance(), file)
        self.play()

