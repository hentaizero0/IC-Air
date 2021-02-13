import time
import copy
import re
import csv
import traceback

from datetime import datetime

# from Azure.Database import Database
from PMSensor.PMSensor import PMSensor
from Thingy.Thingy import Thingy
from Thingy.Delegate import Delegate

def main():
    # database = Database()
    pmSensor = PMSensor()
    delegate = Delegate()
    thingy = Thingy(delegate)

    # database.connect()
    thingy.scan()
    thingy.connect()

    lastPress = -1
    lastTemp = -1
    lastHumid = -1
    lastCO2 = -1
    lastTVOC = -1
    lastPMData = [-1, -1]

    try:
        # assert os.path.exists("./logs/")
        logName = "./logs/" + datetime.now().strftime("%Y-%m-%d_%H:%M") + ".csv"
        csvFile = open(logName, 'w', newline = '')
        csvWriter = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerow(["time"]+["pm2.5"]+["pm10"]+["pressure"]+["temperature"]+["humidity"]+["co2"]+["tvoc"]+["fan"])
        while True:
            timeStamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

            PMData = pmSensor.getData()
            if (PMData != None) and ("," in PMData):
                PMData = PMData.split(',')
                lastPMData = copy.deepcopy(PMData)
            else:
                PMData = copy.deepcopy(lastPMData)
            # end

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
            # envData = "{},{},{},{},{}".format(lastPress, lastTemp, lastHumid, lastCO2, lastTVOC)
            # print(envData)
            # database.insert("{},{},{}".format(timeStamp, PMData, envData))
            csvWriter.writerow([timeStamp]+[PMData[0]]+[PMData[1]]+[lastPress]+[lastTemp]+[lastHumid]+[lastCO2]+[lastTVOC]+["3"])
            print(str(PMData[0])+" "+str(PMData[1])+", Fan:3")
            time.sleep(1)
        # end
    except Exception as error:
        traceback.print_exc()
    finally:
        thingy.disconnect()
    # end
# end

if __name__ == "__main__":
    main()
# end
