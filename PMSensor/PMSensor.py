import serial

class PMSensor:
    def __init__(self):
        self._serial = serial.Serial('/dev/ttyACA0', 9600)
    # end

    def getData(self):
        temp = self._serial.readline()
        if (temp == None or temp == ""):
            return None
        # end

        readSerial = temp.decode('ascii')
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
