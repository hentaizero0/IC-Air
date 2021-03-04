import time
import copy
import re
import csv
import traceback
import os

from datetime import datetime

import PID

import sds011

class PMSensor:
    def __init__(self):
        self._sensorPre = sds011.SDS011('/dev/ttyUSB0', 9600)
        # self._sensorPost = sds011.SDS011('/dev/ttyUSB1', 9600)
    # end

    def start(self):
        self._sensorPre.sleep(sleep = False)
        # self._sensorPost.sleep(sleep = False)
    # end

    def getData(self):
        PMData = []
        PMData += [self._sensorPre.query()]
        # PMData += [self._sensorPost.query()]
        return PMData
    # end

    def stop(self):
        self._sensorPre.sleep(sleep = True)
        # self._sensorPost.sleep(sleep = True)
    # end
# end

timer = 0  # seconds

# TODO: Discuss the PID control with Evan and try to finish it before
# class.
def PID_initialize(p=10.0,i=1.0,d=1.0,setpoint=5.0,sampleTime=1.0):
    pid = PID.PID(p, i, d)
    pid.SetPoint = setpoint
    pid.setSampleTime(sampleTime)
    return pid

def main():
    # iothub.IoTHub()
    # fan = FanController()
    pmSensor = PMSensor()

    pmSensor.start()

    speed = 0
    lastPress = -1
    lastTemp = -1
    lastHumid = -1
    lastCO2 = -1
    lastTVOC = -1
    lastPMDataPre = (-1, -1)
    # lastPMDataPost = (-1, -1)

    pid = PID_initialize(p=10.0,i=1.0,d=1.0,setpoint=5.0)

    try:
        # logName = os.getcwd() + "/logs/" + datetime.now().strftime("%Y-%m-%d_%H:%M") + ".csv"
        # csvFile = open(logName, 'w', newline = '')
        # csvWriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # csvWriter.writerow(["time"]+["pm2.5_pre"]+["pm10_pre"]+["pm2.5_post"]+["pm10_post"]+["pressure"]+["temperature"]+["humidity"]+["co2"]+["tvoc"]+["fan"])
        while True:
            # timeStamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

            PMData = pmSensor.getData()
            if (PMData != ()):
                lastPMDataPre = copy.deepcopy(PMData[0])
                # lastPMDataPost = copy.deepcopy(PMData[1])
            # end

            pid.update(PMData[0][0]) # Pre PM2.5 Update
            speed = pid.output
            speed = max(min(int(abs(speed)), 100), 0)
            # fan.set_speed(speed)

            # csvWriter.writerow([timeStamp]+[lastPMDataPre[0]]+[lastPMDataPre[1]]+[lastPMDataPost[0]]+[lastPMDataPost[1]]+[lastPress]+[lastTemp]+[lastHumid]+[lastCO2]+[lastTVOC]+[speed])

            print("Pre: {}; Fan {}%.".format(PMData[0], speed))

            time.sleep(1)
        # end
    except Exception as error:
        traceback.print_exc()
    finally:
        pmSensor.stop()
        # fan.shutdown()
    # end
# end

if __name__ == "__main__":
    main()
# end
