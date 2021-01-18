from bluepy import btle, thingy52
import binascii
import signal

def shutDown(signum, frame):
    print("# Disconnecting...")
    thingy.disconnect()
    exit(0)
# end

signal.signal(signal.SIGINT, shutDown)


MAC_ADDRESS = None

print("# Looking for Thingy advertisment...")
scanner = btle.Scanner()
devices = scanner.scan(timeout = 3)
for dev in devices:
    # print("Device {} ({}), RSSI={} dB".format(dev.addr, dev.addrType, dev.rssi))
    for (adtype, desc, value) in dev.getScanData():
        # print("  {}, {} = {}".format(adtype, desc, value))
        if (value == "Thingy"):
            print("# Thingy found with address: {}".format(dev.addr))
            MAC_ADDRESS = dev.addr
        # end
    # end
# end

if (MAC_ADDRESS == None):
    print("### ERROR: MAC_ADDRESS is not set (and Thingy was not found)...")
    exit(0)
# end

print("# Creating new delegate class to handle notifications...")
class NewDelegate(btle.DefaultDelegate):
    def handleNotification(self, hnd, data):
        if (hnd == thingy52.e_temperature_handle):
            print("Notification Temperature received: {}".format((self.reprData(data) / 256)))
        # end
        if (hnd == thingy52.e_gas_handle):
            print("Notification Gas received: {}".format(self.reprData(data)))
        # end
        if (hnd == thingy52.e_humidity_handle):
            print("Notification Humidity received: {}".format(self.reprData(data)))
        # end
    # end

    def reprData(self, data):
        return int.from_bytes(data, byteorder = 'big')
    # end
# end

print("# Connecting to Thingy with address {}...".format(MAC_ADDRESS))
thingy = thingy52.Thingy52(MAC_ADDRESS)

# print("# Setting notification handler to default handler...")
#thingy.setDelegate(thingy52.MyDelegate())
print("# Setting notification handler to new handler...")
thingy.setDelegate(NewDelegate())

print("# Configuring and enabling environment notifications...")
thingy.environment.enable()
thingy.environment.configure(temp_int = 1000, humid_int = 1000, gas_mode_int = 2)
thingy.environment.set_temperature_notification(True)
thingy.environment.set_gas_notification(True)
thingy.environment.set_humidity_notification(True)

# print("# Configuring and enabling button press notification...")
# thingy.ui.enable()
# thingy.ui.set_btn_notification(True)

print("# Waiting for three notifications...")
while True:
    thingy.waitForNotifications(timeout = 5)
    thingy.waitForNotifications(timeout = 5)
    thingy.waitForNotifications(timeout = 5)
# end

print("# Disconnecting...")
thingy.disconnect()
