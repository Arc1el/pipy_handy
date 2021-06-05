import cv2 as cv
import numpy as np
import os


def ToHsv(img):
    img_hsv = cv.cvtColor(img_bgr, cv.COLOR_BGR2HSV)

    low = (0, 30, 0)
    high = (24, 255, 255)

    img_mask = cv.inRange(img_hsv, low, high)
    return img_mask

def process(img_bgr):
    img = img_bgr.copy()
    img_bin = ToHsv(img) #cvtcolor로 hsv영역으로 생성, inRange함수를 사용하여 마스크를 만들어 바이너리 이미지 생성

    #이미지 형변환(morphological transformation) https://m.blog.naver.com/samsjang/220505815055
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5)) #타원모양의 커널매트릭스 생성
    img_bin = cv.morphologyEx(img_bin, cv.MORPH_CLOSE, kernel, 1) #closing = dialation(팽창) 수행 후 바로 erosion(침식)수행하여 이미지 크기로 돌려놓음
    cv.imshow("bin_image", img_bin)

cap = cv.VideoCapture(1)
while True:
    ret, img_bgr = cap.read()

    if ret == False:
        break

    img_result = process(img_bgr)

    key = cv.waitKey(1) 

    if key== 27:
        break

cap.release()
cv.destroyAllWindows()
