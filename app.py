import subprocess
import time

from datetime import datetime
from Azure.Database import Database


def main():
    pass
    # 1. add executable mode to each shell script
    subprocess.run(args = ["chmod", "-x","./PMSensor/run.sh", "./Thingy/run.sh", "./Fan/run.sh"])
    database = Database()
    database.connect()

    # 2. run each processes
    try:
        PMSensorProc = subprocess.Popen(["./PMSensor/run.sh"])
        thingyProc = subprocess.Popen(["./Thingy/run.sh"])
        fanProc = subprocess.Popen(["./Fan/run.sh"])

        # TODO: some reuqired operations and debug
        lastPress = 0
        lastTemp = 0
        lastHumid = 0
        lastCO2 = 0
        lastTVOC = 0
        while True:
            pass
            timeStamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            (PMData, PMError) = PMSensorProc.comunicate()
            if PMError:
                raise PMError
            # end

            (thingyData, thingyError) = thingyProc.communicate()
            if thingyError:
                raise thingyError
            # end
            temp = thingyData.split(",")
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
            database.insert("{},{},{}".format(timeStamp, PMData, envData))
            time.sleep(1)
        # end
    except:
        pass
    # end
# end

if "__name__" == "__main__":
    main()
# end
