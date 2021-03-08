import pigpio
import RPi.GPIO as GPIO

class FanController:
    def __init__(self):
        self._GPIO = pigpio.pi()
        self._HSYNC = 18  # actual GPIO
        self._GPIO.set_mode(self._HSYNC, pigpio.ALT5)
        self._GPIO.set_mode(12, pigpio.ALT5)
        # self._GPIO.read(12)

        # set up defalut value
        self._GPIO.hardware_PWM(self._HSYNC, 25000, 1000000)

        # speed thresholds
        # self._speed0 = 0  # 0%
        # self._speed1 = 51  # 20%
        # self._speed2 = 102  # 40%
        # self._speed3 = 153  # 60%
        # self._speed4 = 204  # 80%
        # self._speed5 = 255  # 100%

        self.set_speed(0.2)
    # end

    def set_speed(self, speed):
        self._GPIO.set_PWM_dutycycle(self._HSYNC, int(speed * 255))
    # end

    # FAKE Power Loss Protection
    def shutdown(self):
        self.set_speed(0.0)
    # end

    def get_speed(self):
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(12, GPIO.IN)
        # print(GPIO.input(12))
        return 0.0
        # return self._GPIO.get_PWM_dutycycle(12)
    # end

# end
