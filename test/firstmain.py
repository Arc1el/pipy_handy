import cv2 as cv
import numpy as np
import os
from typing import Final

#rock = 0, scissor = 1, paper = 2
ROCK: Final = 0
SCISSOR: Final = 1
PAPER: Final = 2


def ModeSelect():
    return 0

def DistanceCheck():
    return True

def GetRcp():
    
    while True :
        if DistanceCheck() == True : break

    return 0

def InitOdds(win, lose, total):
    win = 0
    lose = 0
    total = win+lose

def RcpFunc(mode, hand):
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

def LedCtrl(result):
    if result == ROCK:
        pass
    elif result == SCISSOR:
        pass
    elif result == PAPER:
        pass

win, lose, total = 0

while True:
    InitOdds(win, lose, total)

    mode = ModeSelect()

    if mode == 0:
        hand = GetRcp()
        result_hand = RcpFunc(mode, hand)
        LedCtrl(result_hand)

    elif mode == 1:
        hand = GetRcp()
        result_hand = RcpFunc(mode, hand)
        LedCtrl(result_hand)

    elif mode == 2:
        hand = GetRcp()
        result_hand = RcpFunc(mode, hand)
        LedCtrl(result_hand)
