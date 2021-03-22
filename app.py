import FanController
import time
import copy
import re
import csv
import traceback
import os

from datetime import datetime
from azure.iot.device.exceptions import *

from Azure.IoTHub import IoTHub
from FanController.FanController import FanController
from PMSensor.PMSensor import PMSensor
from Thingy.Thingy import Thingy
from Thingy.Delegate import Delegate
from PID import PID

timer = 0  # seconds
pmThreshold = 2.0
nightMode = ['23', '00', '01', '02', '03', '04', '05', '06', '07']

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

# PID initializer
def PID_initialize(p = 10.0, i = 1.0, d = 1.0, setpoint = 5.0, sampleTime = 1.0):
    pid = PID.PID(p, i, d)
    pid.SetPoint = setpoint
    pid.setSampleTime(sampleTime)
    return pid
# end

def main():
    # print ProcessID
    print("Process ID: {}".format(os.getpid()))

    # create module instances
    iothub = IoTHub()
    fan = FanController()
    pmSensor = PMSensor()
    delegate = Delegate()
    thingy = Thingy(delegate)
    pid = PID_initialize(p = 2.0, i = 1.0, d = 1.0, setpoint = 2.0)

    # start some sensors
    pmSensor.start()
    isThingyConnected = thingy.scan()
    if (isThingyConnected):
        thingy.connect()
    # end

    # environment variables
    lastPress = -1
    lastTemp = -1
    lastHumid = -1
    lastCO2 = -1
    lastTVOC = -1
    lastPMDataPre = (-1, -1)
    lastPMDataPost = (-1, -1)

    try:
        # connect to IoTHub
        iothub.connect()

        # create local log
        logName = "/home/pi/Desktop/IC-Air/logs/" + datetime.now().strftime("%Y-%m-%d_%H_%M") + ".csv"
        csvFile = open(logName, 'w', newline = '')
        csvWriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerow(["time"]+["pm2.5_pre"]+["pm10_pre"]+["pm2.5_post"]+["pm10_post"]+["pressure"]+["temperature"]+["humidity"]+["co2"]+["tvoc"]+["fan"])

        # main loop
        while True:
            # time log
            timeStamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

            # get PM data
            PMData = pmSensor.getData()
            if (PMData != ()):
                if PMData[0] != None:
                    lastPMDataPre = copy.deepcopy(PMData[0])
                # end
                if PMData[1] != None:
                    lastPMDataPost = copy.deepcopy(PMData[1])
                # end
            # end

            # set fan speed based on PM data and PID algorithm
            # speed = calculate_fan_speed_rule(lastPMDataPre)
            pid.update(lastPMDataPre[0])

            speed = max(min(int(abs(pid.output)), 80), 0)

            if (datetime.now().strftime("%H") in nightMode):
                speed = max(min(int(abs(pid.output)), 40), 0)
            # end

            # Auto Stop
            if (lastPMDataPre[0] < pmThreshold):
                speed = 0.0
            # end

            fan.set_speed((float(speed) / 100))
            # speed = fan.get_speed()
            # print(fan.get_speed())

            # get other environment data
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

            # write to local log file
            csvWriter.writerow([timeStamp]+[lastPMDataPre[0]]+[lastPMDataPre[1]]+[lastPMDataPost[0]]+[lastPMDataPost[1]]+[lastPress]+[lastTemp]+[lastHumid]+[lastCO2]+[lastTVOC]+[speed])

            # send data to Azure
            data = {
                "time": timeStamp,
                "pm2.5_pre": lastPMDataPre[0],
                "pm10_pre": lastPMDataPre[1],
                "pm2.5_post": lastPMDataPost[0],
                "pm10_post": lastPMDataPost[1],
                "pressure": lastPress,
                "humidity": lastHumid,
                "temperature": lastTemp,
                "CO2": lastCO2,
                "TVOC ppb": lastTVOC,
                "fan": float(speed)
            }

            iothub.send(data)

            # iteratively checking and trying to connect to Thingy
            globals()['timer'] += 1
            if globals()['timer'] == (180):
                globals()['timer'] = 0
                if isThingyConnected == False:
                    isThingyConnected = thingy.scan()
                    if (isThingyConnected):
                        thingy.connect()
                    # end
                # end
            # end

            time.sleep(1)
        # end
    except (ClientError, ConnectionDroppedError, ConnectionFailedError,
            CredentialError, OperationCancelled, ServiceError) :
        # IoTHub exceptions, continue the program
        print("Cannot connect to Azure IoTHub.")
        log = open("/home/pi/Desktop/IC-Air/logs/errorLogs/log_{}.txt".format(datetime.now().strftime("%Y-%m-%d_%H_%M")), 'w')
        traceback.print_exc(file = log)
        log.close()
        traceback.print_exc()
        pass
    except Exception:  # other exceptions, stop the program
        log = open("/home/pi/Desktop/IC-Air/logs/errorLogs/log_{}.txt".format(datetime.now().strftime("%Y-%m-%d_%H_%M")), 'w')
        traceback.print_exc(file = log)
        log.close()
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
