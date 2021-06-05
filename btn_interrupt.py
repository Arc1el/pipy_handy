import RPi.GPIO as GPIO
import time
import lcd as Lcd

WIN = 0
LOSE = 1
RAND = 2
btn_count = 0
retry = 0

def print_lcd(message, line):
    if line == 1:
        Lcd.lcd_string(message, 0x80)
    elif line == 2:
        Lcd.lcd_string(message, 0xC0)

def print_mode(value):
    if value == WIN:
        print_lcd("WIN", 2)
    elif value == LOSE:
        print_lcd("LOSE", 2)
    elif value == RAND:
        print_lcd("RANDOM", 2)

def print_replay(value):
    if value == 0:
        print_lcd("Replay", 2)
    elif value >= 1:
        print_lcd("Nomore", 2)

def my_callback(channel):
    global btn_count
    btn_count = btn_count + 1
    if btn_count == 3:
        btn_count = 0
    print_mode(btn_count)

def my_callback2(channel):
    global retry
    retry = retry + 1
    print_lcd("Nomore", 2)


def set_rcp_mode():
    global btn_count
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(12, GPIO.FALLING, callback=my_callback, bouncetime = 300)
    try:
        time.sleep(5)
        btn_count_copy = btn_count
        btn_count = 0
        GPIO.cleanup()
        return btn_count_copy

    except KeyboardInterrupt:
        GPIO.cleanup()

def replay():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(12, GPIO.FALLING, callback=my_callback2, bouncetime = 300)
    try:
        time.sleep(3)
        GPIO.cleanup()
        if retry == 0:
            return True
        else:
            return False

    except KeyboardInterrupt:
        GPIO.cleanup()