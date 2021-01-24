import time
import copy

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

            temp = thingyData.split(",")
            print(thingyData)
            for i in temp:
                if i == "" or i == None:
                    continue
                # end

                if "Pressure" in i:
                    lastPress = i[11: 18]
                # end

                if "Humidity" in i:
                    lastHumid = i[11: 18]
                # end

                if "Temperature" in i:
                    lastTemp = i[14: 19]
                # end

                if  "CO2" in i:
                    lastCO2 = i[6: 10]
                # end

                if "TVOC ppb" in i:
                    lastTVOC = i[11: 13]
                # end
            # end
            envData = "{},{},{},{},{}".format(lastPress, lastTemp, lastHumid, lastCO2, lastTVOC)
            print("upload data")
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
