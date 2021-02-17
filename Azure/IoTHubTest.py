# Test file for testing Azure IoT Hub connection.

import time
from IoTHub import IoTHub

data = {"a": 1, "b": 2}

iothub = IoTHub()
iothub.connect()
for i in range(120):
    iothub.send(data)
    time.sleep(1)
# end
