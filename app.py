import FanController
import time
import copy
import re
import csv
import traceback
import os

from datetime import datetime

from Azure.IoTHub import IoTHub
from FanController.FanController import FanController
from PMSensor.PMSensor import PMSensor
from Thingy.Thingy import Thingy
from Thingy.Delegate import Delegate

timer = 0  # seconds

# Rule based fan controlling
def calculate_fan_speed_rule(PMData):
    if (PMData == None) or (PMData == (-1, -1)):
        return
    # end

    speed = 0.0

    PM10 = PMData[1]

    # for any tuple in Python, we can do
    #    (x1, x2) < (y1, y2) < (z1, z2)
    # == (x1 < y1 or x2 < y2) and (y1 < z1 or y2 < z2)
    if globals()['timer'] <= 300:
        speed = 0.2
    elif 300 < globals()['timer'] <= 600:
        speed = 0.4
    elif 600 < globals()['timer'] <= 900:
        speed = 0.6
    elif 900 < globals()['timer'] <= 1200:
        speed = 0.8
    else:  # (120.0, 120.0) < PMData
        speed = 0.0
    # end

    # if (PM10 <= 5.0):
    #     speed = 0.5
    # elif (5.0 < PM10 <= 20.0):
    #     speed = 0.5
    # # elif (10.0 < PM10 <= 15.0):
    # #     speed = 0.4
    # # elif (15.0 < PM10 <= 20.0):
    # #     speed = 0.6
    # # elif (20.0 < PM10 <= 25.0):
    # #     speed = 0.8
    # else:  # (120.0, 120.0) < PMData
    #     speed = 0.5
    # # end

    return speed
# end

# TODO: Discuss the PID control with Evan and try to finish it before
# class.
def _PID_control(self, PMData):
    pass
# end

def main():
    # iothub = IoTHub()
    fan = FanController()
    pmSensor = PMSensor()
    delegate = Delegate()
    thingy = Thingy(delegate)

    pmSensor.start()
    # iothub.connect()
    isThingyConnected = thingy.scan()
    if (isThingyConnected):
        thingy.connect()
    # end

    lastPress = -1
    lastTemp = -1
    lastHumid = -1
    lastCO2 = -1
    lastTVOC = -1
    lastPMDataPre = (-1, -1)
    lastPMDataPost = (-1, -1)

    try:
        logName = os.getcwd() + "/logs/" + datetime.now().strftime("%Y-%m-%d_%H:%M") + ".csv"
        csvFile = open(logName, 'w', newline = '')
        csvWriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerow(["time"]+["pm2.5_pre"]+["pm10_pre"]+["pm2.5_post"]+["pm10_post"]+["pressure"]+["temperature"]+["humidity"]+["co2"]+["tvoc"]+["fan"])
        while True:
            timeStamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

            PMData = pmSensor.getData()
            if (PMData != ()):
                if PMData[0] != None:
                    lastPMDataPre = copy.deepcopy(PMData[0])
                # end
                if PMData[1] != None:
                    lastPMDataPost = copy.deepcopy(PMData[1])
                # end
            # end

            speed = calculate_fan_speed_rule(lastPMDataPre)
            fan.set_speed(speed)

            # Actually, here is a call back, but I don't know how to do better.
            if isThingyConnected:
                thingy.run()
                thingyData = copy.deepcopy(delegate.getData())
                delegate.resetData()

                for i in thingyData:
                    if i == "" or i == None:
                        continue
                    # end

                    if "Pressure" in i:
                        lastPress = float(re.findall('\d+.\d+', i)[0])
                    # end

                    if "Humidity" in i:
                        lastHumid = int(re.findall('\d+', i)[0])
                    # end

                    if "Temperature" in i:
                        lastTemp = float(re.findall('\d+.\d+', i)[0])
                    # end

                    if  "CO2" in i:
                        lastCO2 = int(re.findall('\d+', i)[1])
                    # end

                    if "TVOC ppb" in i:
                        lastTVOC = int(re.findall('\d+', i)[0])
                    # end
                # end
            # end

            csvWriter.writerow([timeStamp]+[lastPMDataPre[0]]+[lastPMDataPre[1]]+[lastPMDataPost[0]]+[lastPMDataPost[1]]+[lastPress]+[lastTemp]+[lastHumid]+[lastCO2]+[lastTVOC]+[speed])

            print("Pre: {}; Post: {}; Fan {}%.".format(PMData[0], PMData[1], (speed * 100)))

            globals()['timer'] += 1
            if globals()['timer'] == (1500):
                globals()['timer'] = 0
                isThingyConnected = thingy.scan()
                if (isThingyConnected):
                    thingy.connect()
                # end
            # end

            # data = {
            #     "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            #     "pm2.5_pre": lastPMDataPre[0],
            #     "pm10_pre": lastPMDataPre[1],
            #     "pm2.5_post": lastPMDataPost[0],
            #     "pm10_post": lastPMDataPost[1],
            #     "pressure": lastPress,
            #     "humidity": lastHumid,
            #     "temperature": lastTemp,
            #     "CO2": lastCO2,
            #     "TVOC ppb": lastTVOC
            # }

            # iothub.send(data)
            time.sleep(1)
        # end
    except Exception as error:
        traceback.print_exc()
    finally:
        if isThingyConnected:
            thingy.disconnect()
        # end
        pmSensor.stop()
        fan.shutdown()
    # end
# end

if __name__ == "__main__":
    main()
# end
