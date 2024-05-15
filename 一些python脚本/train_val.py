import os
import random
import shutil

ori_path = r"D:\shuju\pa\北京街镇-数据\城管完成\城管完成\train"
target_path = r"D:\shuju\pa\北京街镇-数据\城管完成\城管完成\val"

list = os.listdir(ori_path);
val_num = int(len(list)*0.2/2)


random.shuffle(list)

for i in range(160):
    filename = list[i]
    if filename=="classes.txt":
        continue
    name = filename.split('.')[0]
    print(name)
    if  not os.path.exists(os.path.join(ori_path,name+'.jpg')):
        continue
    if  not os.path.exists(os.path.join(ori_path,name+'.txt')):
        continue
    shutil.move(os.path.join(ori_path,name+'.txt'),os.path.join(target_path,name+'.txt'))
    shutil.move(os.path.join(ori_path,name+'.jpg'),os.path.join(target_path,name+'.jpg'))
