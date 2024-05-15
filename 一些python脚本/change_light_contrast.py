import os
from shutil import copyfile

import numpy as np
import cv2

ori_path = "D:\shuju\pa\leave_sleepimages_labels\sleep"
target_path = "D:\shuju\pa\leave_sleepimages_labels\sleep_changel_c"

# 调整对比度和亮度
    # alpha = 1.0 表示对比度不变
    # beta = 50 表示增加亮度
alpha = 1.0
beta = 50

files = os.listdir(ori_path)
for file in files:
    if not file.endswith(".txt"):
        imgPath = os.path.join(ori_path, file)
    # 读取图像
        image = cv2.imread(imgPath)
        if image is None:
            print(file)
            continue
    # 使用convertScaleAbs调整图像
        adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        cv2.imwrite(os.path.join(target_path, "lc"+file), adjusted_image)
        copyfile(os.path.join(ori_path,file[:-4]+".txt"),os.path.join(target_path, "lc"+file[:-4]+".txt"))
