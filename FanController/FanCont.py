import pigpio
import time


GPIO = pigpio.pi()

HSYNC = 18
GPIO.set_mode(HSYNC, pigpio.ALT5)
GPIO.hardware_PWM(HSYNC, 25000, 1000000) #set up defalut value
#HSYNC: actual GPIO #
#25000 freq
#1M = 100%

print("real range: {}".format(GPIO.get_PWM_real_range(HSYNC)))
while True:
    #GPIO.set_PWM_frequency(HSYNC, 25000)
    #print(GPIO.get_PWM_dutycycle(18))
    time.sleep(1)
    GPIO.set_PWM_dutycycle(18, 170) #change fan speed, 0~255
    print(GPIO.get_PWM_dutycycle(18))
    # print(HSYNC)
    time.sleep(1)
    print(GPIO.get_PWM_range(HSYNC))
# end

#GPIO.write(HSYNC, 0)
#GPIO.stop()
