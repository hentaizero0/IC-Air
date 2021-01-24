import serial
import csv
import datetime
import time

ser = serial.Serial('/dev/ttyACM0', 9600)
logName = "./" + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M") + ".csv"
with open(logName, 'wb') as csvFile:
    writer = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["time"]+["pm2.5"]+["pm10"])
    while True:
        timeStamp = datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        readSerial = ser.readline()
        if ("No" not in readSerial):
            PMdata = readSerial.split(',')
            print("{},{}".format([PMdata[0]], [PMdata[1][:-2]]))
            writer.writerow([timeStamp]+[PMdata[0]]+[PMdata[1][:-2]])
            time.sleep(1)
    # end
# end
