import pigpio

class FanController:
    def __init__(self):
        self._GPIO = pigpio.pi()
        self._HSYNC = 18  # actual GPIO
        self._GPIO.set_mode(self._HSYNC, pigpio.ALT5)

        # set up defalut value
        self._GPIO.hardware_PWM(self._HSYNC, 25000, 1000000)

        # speed thresholds
        self._speed0 = 0  # 0%
        self._speed1 = 51  # 20%
        self._speed2 = 102  # 40%
        self._speed3 = 153  # 60%
        self._speed4 = 204  # 80%
        self._speed5 = 255  # 100%

        self._set_speed(self._speed2)
    # end

    def _set_speed(self, speed):
        self._GPIO.set_PWM_dutycycle(self._HSYNC, speed)
    # end

    # Rule based fan controlling
    def _rule_control(self, PMData):
        # No data, do not control
        if (PMData == None) or (PMData == (-1, -1)):
            return
        # end

        speed = self._speed2

        # for any tuple in Python, we can do
        #    (x1, x2) < (y1, y2) < (z1, z2)
        # == (x1 < y1 or x2 < y2) and (y1 < z1 or y2 < z2)
        if (PMData <= (5.0, 5.0)):
            speed = self._speed0
        elif ((5.0, 5.0) < PMData <= (30.0, 30.0)):
            speed = self._speed1
        elif ((30.0, 30.0) < PMData <= (60.0, 60.0)):
            speed = self._speed2
        elif ((60.0, 60.0) < PMData <= (90.0, 90.0)):
            speed = self._speed3
        elif ((90.0, 90.0) < PMData <= (120.0, 120.0)):
            speed = self._speed4
        else:  # (120.0, 120.0) < PMData
            speed = self._speed5
        # end

        self._set_speed(speed)  # change fan speed
    # end

    # TODO: Discuss the PID control with Evan and try to finish it before
    # class.
    def _PID_control(self, PMData):
        pass
    # end

    def control(self, PMData):
        self._rule_control(PMData)
        # self._PID_control(PMData)
    # end

    # FAKE Power Loss Protection
    def shutdown(self):
        self._set_speed(self._speed0)
    # end

# end
