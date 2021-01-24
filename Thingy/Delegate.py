import binascii

from bluepy import btle, thingy52

class Delegate(btle.DefaultDelegate):
    def __init__(self):
        super().__init__()
        self._data = []
    # end

    def _str_to_int(self, s):
        """ Transform hex str into int. """
        i = int(s, 16)
        if i >= (2 ** 7):
            i -= (2 ** 8)
        # end
        return i
    # end

    def _extract_pressure_data(self, data):
        """ Extract pressure data from data string. """
        teptep = binascii.b2a_hex(data)
        pressure_int = 0
        for i in range(0, 4):
            pressure_int += (int(teptep[(i * 2): ((i * 2) + 2)], 16) << (8 * i))
        # end
        pressure_dec = int(teptep[-2:], 16)
        return (pressure_int, pressure_dec)
    # end

    def _extract_gas_data(self, data):
        """ Extract gas data from data string. """
        teptep = binascii.b2a_hex(data)
        eco2 = int(teptep[: 2], 16) + (int(teptep[2: 4], 16) << 8)
        tvoc = int(teptep[4: 6], 16) + (int(teptep[6: 8], 16) << 8)
        return (eco2, tvoc)
    # end

    def handleNotification(self, hnd, data):
        if (hnd == thingy52.e_temperature_handle):
            teptep = binascii.b2a_hex(data)
            tempInt = self._str_to_int(teptep[: -2])
            tempDec = int(teptep[-2:], 16)
            tempTotal = 'Temperature: {}.{} degCelsius'.format(tempInt, tempDec)
            self._data += [tempTotal]
            print(tempTotal, end = ",")
        # end

        if (hnd == thingy52.e_pressure_handle):
            (pressure_int, pressure_dec) = self._extract_pressure_data(data)
            pressure = 'Pressure: {}.{} hPa'.format(pressure_int, pressure_dec)
            self._data += [pressure]
            print(pressure, end = ",")
        # end

        if (hnd == thingy52.e_humidity_handle):
            teptep = binascii.b2a_hex(data)
            humidity = 'Humidity: {} %'.format(self._str_to_int(teptep))
            self._data += [humidity]
            print(humidity, end = ",")
        # end

        if (hnd == thingy52.e_gas_handle):
            (eco2, tvoc) = self._extract_gas_data(data)
            gas = 'CO2: {} ppm,TVOC ppb: {} %'.format(eco2, tvoc)
            self._data += gas.split(',')
            print(gas, end = ",")
        # end
    # end

    def getData(self):
        return self._data
    # end

    def resetData(self):
        self._data = []
    # end
# end
