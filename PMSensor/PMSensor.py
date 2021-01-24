import serial

class PMSensor:
    def __init__(self):
        self._serial = serial.Serial('/dev/ttyACM0', 9600)
    # end

    def getData(self):
        readSerial = self._serial.readline.decode('ascii')
        PMData = None
        if ("No" not in readSerial):
            # print(readSerial)
            PMData = readSerial[:-2]
            # PMData = "{},{}".format(PMData[0], PMData[1][:-2])
            # print("{},{}".format(PMData[0], PMData[1][:-2]))
        # end
        return PMData
    # end
# end
