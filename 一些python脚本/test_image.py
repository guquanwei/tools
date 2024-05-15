import os

import cv2

path = r'D:\shuju\pa\zhihuigongdi\20240306\jianzhujixie\101_bulldozer2'

list = os.listdir(path)
for i in list:
    imgPath = os.path.join(path, i)
    img = cv2.imread(imgPath);

