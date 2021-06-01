import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def my_callback(channel):
    print("btn pressed")
    
GPIO.add_event_detect(12, GPIO.FALLING, callback=my_callback)

try:
    while True:
        time.sleep(30)

except KeyboardInterrupt:
    GPIO.cleanup()
    
GPIO.cleanup()
