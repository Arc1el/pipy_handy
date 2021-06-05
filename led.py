import RPi.GPIO as GPIO

def led_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)


def rock_on() :
    GPIO.output(16, True)

def rock_off() :
    GPIO.output(16, False)

def scissor_on() :
    GPIO.output(16, True)
    GPIO.output(20, True)

def scissor_off() :
    GPIO.output(16, False)
    GPIO.output(20, False)

def paper_on() :
    GPIO.output(16, True)
    GPIO.output(20, True)
    GPIO.output(21, True)

def paper_off() :
    GPIO.output(16, False)
    GPIO.output(20, False)
    GPIO.output(21, False)

def led_ctrl(led, mode):
    led_setup()
    if mode == "on":
        if led == 0:
            rock_on()
        elif led == 1:
            scissor_on()
        elif led == 2:
            paper_on()
    elif mode == "off":
        if led == 0:
            rock_off()
        elif led == 1:
            scissor_off()
        elif led == 2:
            paper_off()
