import time

from datetime import datetime

from Azure.IoTHub import IoTHub

iothub = IoTHub()
iothub.connect()

while True:
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "pm2.5_pre": 1.0,
        "pm10_pre": 2.0,
        "pm2.5_post": 3.0,
        "pm10_post": 4.0,
        "pressure": 5.0,
        "humidity": 6.0,
        "temperature": 7.0,
        "CO2": 8.0,
        "TVOC ppb": 9.0,
        "fan": 0.5
        }

    print(data)
    iothub.send(data)

    time.sleep(2)
# end
