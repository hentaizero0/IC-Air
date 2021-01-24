from bluepy import btle, thingy52

from Thingy import Delegate

class Thingy:
    def __init__(self, delegate = None):
        self._MAC_ADDRESS = None
        self._thingy = None
        self._delegate = delegate
    # end

    def scan(self):
        print("# Looking for Thingy advertisment...")
        scanner = btle.Scanner()
        devices = scanner.scan(timeout = 3)
        for dev in devices:
            # print("Device {} ({}), RSSI={} dB".format(dev.addr, dev.addrType, dev.rssi))
            for (adtype, desc, value) in dev.getScanData():
                # print("  {}, {} = {}".format(adtype, desc, value))
                if (value == "Thingy"):
                    print("# Thingy found with address: {}".format(dev.addr))
                    self._MAC_ADDRESS = dev.addr
                # end
            # end
        # end

        if (self._MAC_ADDRESS == None):
            print("### ERROR: MAC_ADDRESS is not set (and Thingy was not found)...")
            exit(0)
        # end
    # end

    def connect(self):
        print("# Connecting to Thingy with address {}...".format(self._MAC_ADDRESS))
        self._thingy = thingy52.Thingy52(self._MAC_ADDRESS)
        # print("# Setting notification handler to default handler...")
        # self._thingy.setDelegate(thingy52.MyDelegate())
        print("# Setting notification handler to new handler...")
        if self._delegate == None:
            self._delegate = Delegate()
        # end
        self._thingy.setDelegate(self._delegate)

        print("# Configuring and enabling environment notifications...")
        self._thingy.environment.enable()
        self._thingy.environment.configure(temp_int = 1000, humid_int = 1000, gas_mode_int = 2, press_int = 1000)
        self._thingy.environment.set_temperature_notification(True)
        self._thingy.environment.set_gas_notification(True)
        self._thingy.environment.set_humidity_notification(True)
        self._thingy.environment.set_pressure_notification(True)

        # print("# Configuring and enabling battery data...")
        # self._thingy.battery.enable()
    # end

    def run(self):
        print("# Waiting for notifications...")
        self._thingy.waitForNotifications(timeout = 5)
        self._thingy.waitForNotifications(timeout = 5)
        self._thingy.waitForNotifications(timeout = 5)
        self._thingy.waitForNotifications(timeout = 5)
    # end

    def disconnect(self):
        print("# Disconnecting...")
        self._thingy.disconnect()
        del self._thingy
    # end
# end
