import pulsectl


class OutputControl():
    raise NotImplementedError
    def SetVolumeAll(self):
        pass
    def SetVolumeSink(self):
        pass
    def CreateCombinedSink(self):
        pass
    def SetDefaultOutput(self):
        pass


class Play(OutputControl):
    def __init__(self, ):
