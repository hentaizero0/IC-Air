import sds011

class PMSensor:
    def __init__(self):
        self._sensorPre = sds011.SDS011('/dev/ttyUSB0', 9600)
        self._sensorPost = sds011.SDS011('/dev/ttyUSB1', 9600)
    # end

    def start(self):
        self._sensorPre.sleep(sleep = False)
        self._sensorPost.sleep(sleep = False)
    # end

    def getData(self):
        PMData = []
        PMData += [self._sensorPre.query()]
        PMData += [self._sensorPost.query()]
        return PMData
    # end

    def stop(self):
        self._sensorPre.sleep(sleep = True)
        self._sensorPost.sleep(sleep = True)
    # end
# end
