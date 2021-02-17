# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for full license information.
import json

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
from azure.iot.device import IoTHubDeviceClient, Message



# Define the JSON message to send to IoT Hub.

class IoTHub:
    def __init__(self):
        # The device connection string to authenticate the device with your IoT hub.
        self._connectionString = "HostName=ZephyrAir.azure-devices.net;DeviceId=Purifer;SharedAccessKey=4VqF3ln3HqyUHkh76zmXdWxVLI9FB9/4OBy6ChtMXCQ="
        self._client = None
    # end

    # Create an IoT Hub client
    def connect(self):
        self._client = IoTHubDeviceClient.create_from_connection_string(self._connectionString)

        # No error checking required because the IoTHub will rasie the error.
    # end

    def send(self, data):
        jsonData = json.dumps(data)
        message = Message(jsonData)
        self._client.send_message(message)
    # end
# end
