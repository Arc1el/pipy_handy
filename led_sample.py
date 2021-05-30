import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

try:
    while True:
        GPIO.output(21, True)
        sleep(0.5)
        GPIO.output(21, False)
        sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
