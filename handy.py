import cv2 as cv
import numpy as np
import os
import time

def to_hsv(img):
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    low = (0, 30, 0)
    high = (20, 255, 255) #20, 24

    img_mask = cv.inRange(img_hsv, low, high)
    return img_mask

def get_max_area(contours):
    max_contour = None
    max_area = -1

    #가장큰 컨투어만 찾기 https://docs.opencv.org/4.3.0/dd/d49/tutorial_py_contour_features.html
    for contour in contours:
        area = cv.contourArea(contour) #외곽선이 감싸는 면적 반환
        x, y, w, h = cv.boundingRect(contour) # 최소크기 사각형(바운딩박스 반환)

        if (w * h) * 0.4 > area:
            continue
        if w > h:
            continue
        if area > max_area:
            max_area = area
            max_contour = contour
    
    if max_area < 10000:
        max_area = -1
    
    return max_area, max_contour

def calculate_angle(A, B):
    A_norm = np.linalg.norm(A)
    B_norm = np.linalg.norm(B)
    C = np.dot(A,B)

    angle = np.arccos(C/(A_norm*B_norm))*180/np.pi
    return angle

def distance_between_two_points(start, end):

    x1,y1 = start
    x2,y2 = end
 
    return int(np.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2)))


def get_finger_position(max_contour, img):
    points1 = []
    #모멘트 사용하여 손가락포지션 계산 https://076923.github.io/posts/Python-opencv-25/
    M = cv.moments(max_contour)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    #근사화, 컨벡스 헐 https://deep-learning-study.tistory.com/232
    max_contour = cv.approxPolyDP(max_contour,0.02*cv.arcLength(max_contour,True),True) #외곽선 근사화(단순화)
    hull = cv.convexHull(max_contour) #컨벡스 헐 반환

    for point in hull:
        if cy > point[0][1]:
            points1.append(tuple(point[0])) 

    hull = cv.convexHull(max_contour, returnPoints=False)
    defects = cv.convexityDefects(max_contour, hull) # 컨벡스 디펙트 반환
    '''
    if defects is None:
        return -1,None
    '''

    if defects is None:
        return -1

    points2=[]
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i, 0]
        start = tuple(max_contour[s][0])
        end = tuple(max_contour[e][0])
        far = tuple(max_contour[f][0])

        angle = calculate_angle( np.array(start) - np.array(far), np.array(end) - np.array(far))
        if angle < 90:
            if start[1] < cy:
                points2.append(start)
            if end[1] < cy:
                points2.append(end)

    points = points1 + points2
    points = list(set(points))

    new_points = []
    for p0 in points:
    
        i = -1
        for index,c0 in enumerate(max_contour):
            c0 = tuple(c0[0])

            if p0 == c0 or distance_between_two_points(p0,c0)<20:
                i = index
                break

        if i >= 0:
            pre = i - 1
            if pre < 0:
                pre = max_contour[len(max_contour)-1][0]
            else:
                pre = max_contour[i-1][0]
            
            next = i + 1
            if next > len(max_contour)-1:
                next = max_contour[0][0]
            else:
                next = max_contour[i+1][0]


            if isinstance(pre, np.ndarray):
                    pre = tuple(pre.tolist())
            if isinstance(next, np.ndarray):
                next = tuple(next.tolist())

            
            angle = calculate_angle( np.array(pre) - np.array(p0), np.array(next) - np.array(p0))     

            if angle < 90:
                new_points.append(p0)
    
    
    return len(new_points)
    #return 1,new_points,


def process_handy(img_bgr):
    img = img_bgr.copy()
    img_bin = to_hsv(img) #cvtcolor로 hsv영역으로 생성, inRange함수를 사용하여 마스크를 만들어 바이너리 이미지 생성

    #이미지 형변환(morphological transformation) https://m.blog.naver.com/samsjang/220505815055
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5)) #타원모양의 커널매트릭스 생성
    img_bin = cv.morphologyEx(img_bin, cv.MORPH_CLOSE, kernel, 1) #closing = dialation(팽창) 수행 후 바로 erosion(침식)수행하여 이미지 크기로 돌려놓음

    #cv.imshow("bin_image", img_bin)
   

    #컨투어를 사용하여 손모양만 캐치 https://m.blog.naver.com/samsjang/220534805843, https://m.blog.naver.com/samsjang/220516697251
    contours, hierarchy = cv.findContours(img_bin, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) # 이미지의 바깥쪽 contour검출, 모서리점만 남기고 다 버림.

    #for cnt in contours:
        #cv.drawContours(img_bin, [cnt], 0, (255, 0, 0), 3)

    max_area, max_contour = get_max_area(contours)
    
    if max_area == -1:
        return -1

    #cv.drawContours(img, [max_contour], 0, (0, 255, 0), 3)

    len = get_finger_position(max_contour, img)

    return len
    

def handy():
    cap = cv.VideoCapture(0)
    while True:

        ret, img_bgr = cap.read()

        if ret == False:
            break

        result = process_handy(img_bgr)
        if type(result) == int:
            
            if result < 2 and result != -1:
                #print("바위")
                cap.release()
                return 0
            elif result >=2 and result < 5 and result != -1:
                #print("가위")
                cap.release()
                return 1
            elif result >= 5 and result != -1:
                #print("보")
                cap.release()
                return 2
            else:
                #print("감지되지않음")
                cap.release()
                return -1
            
        key = cv.waitKey(1) 
        if key== 27:
            break

handy()