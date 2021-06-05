import os
import time
import lcd as Lcd
import led as Led
import btn_interrupt as Btn
import handy as Handy
import RPi.GPIO as GPIO
import numpy as np

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)


#rock = 0, scissor = 1, paper = 2
ROCK = 0
SCISSOR = 1
PAPER = 2


def print_lcd(message, line):
    if line == 1:
        Lcd.lcd_string(message, 0x80)
    elif line == 2:
        Lcd.lcd_string(message, 0xC0)

def timer_three():
    for i in range(3, 0, -1):
            print(i)
            print_lcd(i, 2)
            time.sleep(0.5)

def env_check():
    Lcd.main()
    print("환경을 체크합니다. 지시에 따르세요")
    print_lcd("Enviroment check", 1)
    print_lcd("Follow the order", 2)
    time.sleep(2)
    while True:
        print("가위를 내세요")
        print_lcd("Throw SCISSORS", 1)
        timer_three()
        myhand = Handy.handy()

        if myhand == SCISSOR:
            pass
        else:
            print("손, 밝기 등을 조절하여 다시 시도해주세요")
            print_lcd("Try again by", 1)
            print_lcd("adjusting hands", 2)

            time.sleep(2)
            continue

        print("바위를 내세요")
        print_lcd("Throw a ROCK", 1)
        timer_three()

        myhand = Handy.handy()

        if myhand == ROCK:
            pass
        else:
            print("손, 밝기 등을 조절하여 다시 시도해주세요")
            print_lcd("Try again by", 1)
            print_lcd("adjusting hands", 2)
            time.sleep(2)
            continue

        print("보를 내세요")
        print_lcd("Throw PAPER", 1)
        timer_three()
        myhand = Handy.handy()

        if myhand == PAPER:
            break
        else:
            print("손, 밝기 등을 조절하여 다시 시도해주세요")
            print_lcd("Try again by", 1)
            print_lcd("adjusting hands", 2)
            time.sleep(2)
            continue

    print("환경이 양호합니다. 게임을 진행합니다.")
    print_lcd("Setup Complete", 1)
    print_lcd("Let's play game", 2)
    time.sleep(2)

    return True

def init_odds(win, lose, total):
    win = 0
    lose = 0
    total = win+lose

def rcp_func(mode, hand):
    if mode == 0: #WIN
        if hand == ROCK : return PAPER
        elif hand == SCISSOR : return ROCK
        elif hand == PAPER : return SCISSOR

    elif mode == 1: #LOSE
        if hand == ROCK : return SCISSOR
        elif hand == SCISSOR : return PAPER
        elif hand == PAPER : return ROCK

    elif mode == 2: #RAND
        return np.random.randint(2)

def const_to_string(value):
    if value == ROCK:
        return "ROCK"
    elif value == SCISSOR:
        return "SCISSOR"
    elif value == PAPER:
        return "PAPER"

def mode_select():
    mode = Btn.set_rcp_mode()
    return mode

def gamestart(mode):
    while True :
            if env_check() == True : break
    counter = 0
    win = 0
    lose = 0
    draw = 0
    while True :
            Lcd.main()
            counter = counter + 1
            print_lcd("Play R C P !", 1)
            timer_three()
            myhand = Handy.handy()
            print(myhand)
            
            if myhand == -1:
                while True:
                    print("다시 시도합니다.")
                    print_lcd("Retry !", 1)
                    timer_three()
                    myhand = Handy.handy()
                    print(myhand)
                    if myhand != -1:
                        break
                      
            
            rasphand = rcp_func(mode, myhand)
            Led.led_ctrl(rasphand, "on")
            print(f"당신이 낸 손 : {const_to_string(myhand)}, 라즈베라피이가 낸 손 : {const_to_string(rasphand)}")

            you_string = "You : " + const_to_string(myhand)
            rasp_string = "Raspi : " + const_to_string(rasphand)

            print_lcd(you_string, 1)
            print_lcd(rasp_string, 2)

            time.sleep(2)

            
            if mode == 0:
                win = counter
                lose = 0
                counter_string1 = "Count : " + str(counter)
                counter_string2 = "Win : " + str(win) + " Lose : " + str(lose)

            elif mode == 1:
                win = 0
                lose = counter
                counter_string1 = "Count : " + str(counter)
                counter_string2 = "Win : " + str(win) + " Lose : " + str(lose)

            elif mode == 2:
                if myhand == ROCK and rasphand == PAPER:
                    win = win + 1
                elif myhand == SCISSOR and rasphand == ROCK:
                    win = win + 1
                elif myhand == PAPER and rasphand == SCISSOR:
                    win = win + 1
                elif myhand == rasphand:
                    draw = draw + 1
                else:
                    lose = lose + 1

                counter_string1 = "Count : " + str(counter)
                counter_string2 = "Win : " + str(win) + " Lose : " + str(lose)

            print_lcd(counter_string1, 1)
            print_lcd(counter_string2, 2)

            time.sleep(3)

            print_lcd("Wanna Stop ?", 1)
            print_lcd("Press Btn ----->", 2)

            replay = Btn.replay()
            Led.led_ctrl(rasphand, "off")
     
            if replay == False:
                break
            elif replay == True:
                continue
    return counter, win, lose, draw

def display_count(counter, win, lose, draw):
    Lcd.main()
    final_string1 = "Cntt : " + str(counter) +" Draw : " + str(draw)
    final_string2 = "Win : " + str(win) + " Lose : " + str(lose)
    print_lcd(final_string1, 1)
    print_lcd(final_string2, 2)
    time.sleep(3)

def main():
    Lcd.main()
    print("Select Mode - Default : WIN")
    print_lcd("Select Mode", 1)
    print_lcd("WIN", 2)
    mode = mode_select()

    if mode == 0:
        counter, win, lose, draw = gamestart(mode)
        display_count(counter, win, lose, draw)
    elif mode == 1:
        counter, win, lose, draw = gamestart(mode)
        display_count(counter, win, lose, draw)
    elif mode == 2:
        counter, win, lose, draw = gamestart(mode)
        display_count(counter, win, lose, draw)

main()
