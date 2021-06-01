import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

try:
    while True:
        GPIO.output(16, True)
        sleep(0.5)
        GPIO.output(20, True)
        sleep(0.5)
        GPIO.output(21, True)
        sleep(0.5)
        GPIO.output(16, False)
        GPIO.output(20, False)
        GPIO.output(21, False)
        sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
