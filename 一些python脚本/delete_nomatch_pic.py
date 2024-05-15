import os
import shutil

labels_path = r'D:\shuju\pa\zhihuigongdi\20240306\社会车辆-10--- - 副本\labels'
pic_path = r'D:\shuju\pa\zhihuigongdi\20240306\社会车辆-10--- - 副本\3_motorbike_摩托车4'
targetPath = r'D:\shuju\pa\zhihuigongdi\20240306\社会车辆-10--- - 副本\3_motorbike_摩托车3'

jpgs = os.listdir(pic_path)
for jpg in jpgs:
    name = os.path.splitext(jpg)[0]
    jpg_path = os.path.join(pic_path,jpg)
    label_path = os.path.join(labels_path,name+'.txt')
    if os.path.exists(jpg_path) and not os.path.exists(label_path):
        os.remove(jpg_path)
        # shutil.move(jpg_path, targetPath+"/"+jpg)
        print(jpg_path)



