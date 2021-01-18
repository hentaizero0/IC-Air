from bluepy import btle, thingy52
import binascii
import signal
import sys

def main(): 
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

    print("# Connecting to Thingy with address {}...".format(MAC_ADDRESS))
    thingy = thingy52.Thingy52(MAC_ADDRESS)

    try:
        print("# Setting notification handler to default handler...")
        thingy.setDelegate(thingy52.MyDelegate())
        # print("# Setting notification handler to new handler...")
        # thingy.setDelegate(thingy52.MyDelegate())

        print("# Configuring and enabling environment notifications...")
        thingy.environment.enable()
        thingy.environment.configure(temp_int = 1000, humid_int = 1000, gas_mode_int = 2, press_int = 1000)
        thingy.environment.set_temperature_notification(True)
        thingy.environment.set_gas_notification(True)
        thingy.environment.set_humidity_notification(True)
        thingy.environment.set_pressure_notification(True)

        print("# Configuring and enabling battery data...")
        thingy.battery.enable()

        print("# Waiting for three notifications...")
        while thingy.battery.read() > 0:
            thingy.waitForNotifications(timeout = 5)
            thingy.waitForNotifications(timeout = 5)
            thingy.waitForNotifications(timeout = 5)
            thingy.waitForNotifications(timeout = 5)
        else:
            raise ValueError(thingy.battery.read())
        # end
    except KeyboardInterrupt:
        print("Manually stop.")
    except ValueError:
        print("Run out of Battery.")
    finally:
        print("# Disconnecting...")
        thingy.disconnect()
        del thingy
    # end
# end

if __name__ == '__main__':
    main()
# end