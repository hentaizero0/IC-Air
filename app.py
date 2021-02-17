import time
import copy
import re
import csv
import traceback

from datetime import datetime

# from IoTHub.IoTHub import IoTHub
from FanController.FanController import FanController
from PMSensor.PMSensor import PMSensor
from Thingy.Thingy import Thingy
from Thingy.Delegate import Delegate

def main():
    # iothub.IoTHub()
    fan = FanController()
    pmSensor = PMSensor()
    delegate = Delegate()
    thingy = Thingy(delegate)

    pmSensor.start()
    # iothub.connect()
    thingy.scan()
    thingy.connect()

    lastPress = -1
    lastTemp = -1
    lastHumid = -1
    lastCO2 = -1
    lastTVOC = -1
    lastPMDataPre = (-1, -1)
    lastPMDataPost = (-1, -1)

    try:
        logName = "./logs/" + datetime.now().strftime("%Y-%m-%d_%H:%M") + ".csv"
        csvFile = open(logName, 'w', newline = '')
        csvWriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerow(["time"]+["pm2.5_pre"]+["pm10_pre"]+["pm2.5_post"]+["pm10_post"]+["pressure"]+["temperature"]+["humidity"]+["co2"]+["tvoc"]+["fan"])
        while True:
            timeStamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

            PMData = pmSensor.getData()
            if (PMData != ()):
                lastPMDataPre = copy.deepcopy(PMData[0])
                lastPMDataPost = copy.deepcopy(PMData[1])
            # end

            fan.control(lastPMDataPre)

            # Actually, here is a call back, but I don't know how to do better.
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

            csvWriter.writerow([timeStamp]+[lastPMDataPre[0]]+[lastPMDataPre[1]]+[lastPMDataPost[0]]+[lastPMDataPost[1]]+[lastPress]+[lastTemp]+[lastHumid]+[lastCO2]+[lastTVOC]+["3"])

            print(str(PMData[0])+" "+str(PMData[1])+", Fan:3")

            time.sleep(1)
        # end
    except Exception as error:
        traceback.print_exc()
    finally:
        thingy.disconnect()
        pmSensor.stop()
        fan.shutdown()
    # end
# end

if __name__ == "__main__":
    main()
# end
