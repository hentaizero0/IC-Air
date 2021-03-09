import pigpio

GPIO = pigpio.pi()
GPIO.set_mode(18, pigpio.ALT5)
GPIO.set_PWM_dutycycle(18, int(0.0 * 255))
