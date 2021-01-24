import binascii

from bluepy import btle, thingy52

class NewDelegate(btle.DefaultDelegate):

    def _str_to_int(self, s):
        """ Transform hex str into int. """
        i = int(s, 16)
        if i >= 2**7:
            i -= 2**8
        return i
    # end

    def _extract_pressure_data(self, data):
        """ Extract pressure data from data string. """
        teptep = binascii.b2a_hex(data)
        pressure_int = 0
        for i in range(0, 4):
                pressure_int += (int(teptep[i*2:(i*2)+2], 16) << 8*i)
        pressure_dec = int(teptep[-2:], 16)
        return (pressure_int, pressure_dec)
    # end

    def _extract_gas_data(self, data):
        """ Extract gas data from data string. """
        teptep = binascii.b2a_hex(data)
        eco2 = int(teptep[:2], 16) + (int(teptep[2:4], 16) << 8)
        tvoc = int(teptep[4:6], 16) + (int(teptep[6:8], 16) << 8)
        return (eco2, tvoc)
    # end

    def handleNotification(self, hnd, data):
        if (hnd == thingy52.e_temperature_handle):
            teptep = binascii.b2a_hex(data)
            tempInt = self._str_to_int(teptep[:-2])
            tempDec = int(teptep[-2:], 16)
            print('Temperature: {}.{} degCelsius'.format(tempInt, tempDec), end = ",")
        # end

        if (hnd == thingy52.e_pressure_handle):
            (pressure_int, pressure_dec) = self._extract_pressure_data(data)
            print('Pressure: {}.{} hPa'.format(pressure_int, pressure_dec), end = ",")
        # end

        if (hnd == thingy52.e_humidity_handle):
            teptep = binascii.b2a_hex(data)
            print('Humidity: {} %'.format(self._str_to_int(teptep)), end = ",")
        # end

        if (hnd == thingy52.e_gas_handle):
            (eco2, tvoc) = self._extract_gas_data(data)
            print('CO2: {} ppm,TVOC ppb: {} %'.format(eco2, tvoc), end = ",")
        # end
    # end
# end


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
        # print("# Setting notification handler to default handler...")
        # thingy.setDelegate(thingy52.MyDelegate())
        print("# Setting notification handler to new handler...")
        thingy.setDelegate(NewDelegate())

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
            print()
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
