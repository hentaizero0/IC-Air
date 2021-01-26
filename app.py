import time
import copy
import re

from datetime import datetime

from Azure.Database import Database
from PMSensor.PMSensor import PMSensor
from Thingy.Thingy import Thingy
from Thingy.Delegate import Delegate

def main():
    database = Database()
    pmSensor = PMSensor()
    delegate = Delegate()
    thingy = Thingy(delegate)

    database.connect()
    thingy.scan()
    thingy.connect()

    lastPress = 0
    lastTemp = 0
    lastHumid = 0
    lastCO2 = 0
    lastTVOC = 0

    try:
        while True:
            timeStamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

            PMData = pmSensor.getData()
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
            envData = "{},{},{},{},{}".format(lastPress, lastTemp, lastHumid, lastCO2, lastTVOC)
            print(envData)
            database.insert("{},{},{}".format(timeStamp, PMData, envData))
            time.sleep(1)
        # end
    except Exception as error:
        print(error)
    finally:
        thingy.disconnect()
    # end
# end

if __name__ == "__main__":
    main()
# end
