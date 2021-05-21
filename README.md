# pipy_handy
raspi 4b + openCV

PINTO의 custom bazel, mediapipe 설치 - https://ahnsun98.tistory.com/6

PINTO의 custom TensorflowV2 - https://github.com/PINTO0309/Tensorflow-bin/#usage

MediaPipe in Python - https://google.github.io/mediapipe/getting_started/python.html

MediaPipe Python on aarch64 (Raspberry Pi4 custom. experimental) - https://github.com/jiuqiant/mediapipe_python_aarch64


#1차시도 tensorflow + opencv-python + bazel2.0.0 + mediapipe
#lowversion. required for bazel 3.1.7

#2차시도 tensorflow +opencv-python + bazel(using docker) + mediapipe

#3차시도 tensorflow(custom mediapipe) + opencv-contrib-python + bazel 3.1.7 + mediapipe
#설치성공(부분 부분컴파일 실패) + import오류. 제대로 설치되지 않은듯함

#3차시도 tensorflow(cp37) + bazel 3.1.7 + medaipipe(using custom aarch64 build) + (opencv-contrib-python)
#https://github.com/jiuqiant/mediapipe_python_aarch64
#setup과정에서시간이 너무오래걸림. 실패라고 판단. tf2 사용하였는데 tflite를 진행하는것보고 중단 결정.

![image](https://user-images.githubusercontent.com/8403172/118922646-5d25c280-b975-11eb-82be-68edb77ecde6.png)


#4차시도. 한번 진행할때 마다마다  너무 시간이 오래걸려서 이번테스트까지만 해보고 방향성을 바꿔야할것 같다. (video를 받아와서 desktop에서 처리)
#tensorflowlite + bazel + mediapipe(using custom aarch64 build) + opencv-python

![image](https://user-images.githubusercontent.com/8403172/118963515-780e2c00-b9a1-11eb-905f-fecb38e92259.png)

다른방법을 생각해야될것같다

opencv의 색상추출을 사용. 손가락을 몇개 폈는지 인식이 가능하다. (단, 손의 정면에서만 인식이 가능할것 같다)

최대한 독립된 기기로써의 프로그래밍을 하기위해서 해당방법을 사용하는 방향으로 진행할것이다.

![image](https://user-images.githubusercontent.com/8403172/119071923-9cabe780-ba25-11eb-817c-3b182141c1d4.png)

인식률이 좋지않다. 색상추출을 사용하기때문에 주변환경의 영향이 많다. yolov5를 사용하는쪽으로 생각해보아야겠다.

yolov5로 작성된 모델 - https://drive.google.com/file/d/15F0N0VyCqBsnVosfSb6GOjn3oL7OlvHt/view?usp=sharing

![image](https://user-images.githubusercontent.com/8403172/119111797-6179da80-ba5e-11eb-98c3-34bb202bb4a0.png)

성능 한계때문에 적합하지 않다. pythorch를 사용하지않는 yolov3로 변경해서 진행해봐야겠다.
yolo자체가 cpu로 빠른순간을 캐치하기가 힘들다. opencv만을 사용하기도 하였다.
