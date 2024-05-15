import os

import cv2

ori_path = r"D:\shuju\pa\zhihuigongdi\20240306\jianzhujixie\101_bulldozer2"
target_path = r"D:\shuju\pa\zhihuigongdi\20240306\jianzhujixie\101_2_pics"

files = os.listdir(ori_path)
for file in files:

    if file.endswith(".txt"):
        if file == "classes.txt":
            continue
        filePath = os.path.join(ori_path, file)
        with open(filePath,"r") as f:
            annos = f.readlines();
        annos_mirror = ""
        for anno in annos:
            if anno=="":
                break
            label = anno.split(" ")
            label[1] = str(round(1-float(label[1]),6))
            label_mirror = label[0]+" "+label[1]+" "+label[2]+" "+label[3]+" "+label[4]+"\n"
            annos_mirror += label_mirror
        mirror_labelPath = os.path.join(target_path,file[:-4]+"131"+file[-4:])
        with open(mirror_labelPath,"w") as f2:
            f2.write(annos_mirror)

    else:
        imgPath = os.path.join(ori_path, file)
        img = cv2.imread(imgPath)
        if img is None:
            filePath = os.path.join(ori_path, file[:-4]+".txt")
            os.remove(filePath)
            print(file)
            continue
        mirror_img = cv2.flip(img, 1)
        mirror_imgPath = os.path.join(target_path,file[:-4]+"131"+file[-4:])
        cv2.imwrite(mirror_imgPath,mirror_img)