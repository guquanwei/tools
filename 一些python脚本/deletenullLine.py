# coding:utf-8
import os

path = r"D:\shuju\pa\zhihuigongdi\20240306\jianzhujixie\101_2_pics\la"
newPath = r"D:\shuju\pa\zhihuigongdi\20240306\jianzhujixie\101_2_pics\la2"
labels = os.listdir(path)
for label in labels:
    label_path = os.path.join(path, label)
    new_label_path = os.path.join(newPath, label)
    file1 = open(label_path, 'r')   # 打开要去掉空行的文件
    file2 = open(new_label_path, 'w')  # 生成没有空行的文件

    for line in file1.readlines():
        if line == '\n':
            line = line.strip('\n')
        file2.write(line)


