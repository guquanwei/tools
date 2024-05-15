# -*- coding: utf-8 -*-
#
import argparse, io, copy, time, yaml, base64, re, os, glob, shutil, pathlib
from pathlib import Path
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
IMAGEFORMAT = ['.jpg', '.jpeg', '.png', '.bmp',  '.cur', '.gif', '.ico', '.jfif', '.pcx', '.tiff', '.tga', '.webp', '.yuv']
dir = ''
subdirs = []
def opendir():
    global dir, subdirs
    dir = filedialog.askdirectory()  # 选择目录，返回目录名
    if dir.strip() != '':
        dirpath.set(dir)  # 设置变量outputpath的值
        p0 = glob.glob(str(Path(dir) / '**'))
        subdirs = [pathlib.PureWindowsPath(i).as_posix() for i in p0]
        for item in subdirs:
            # treeview.insert(END, item)
            treeview.insert("", "end", text=item)
    else:
        print("do not choose Dir")
def create_train_val_txt():
    global dir, subdirs
    select = treeview.selection()
    train2017_lst, val2017_lst = [], []
    for i in select:
        subdir = treeview.item(i, "text")
        print(subdir)
        p0 = glob.glob(str(Path(subdir) / '**' / '*.*'), recursive=True)
        lst = [pathlib.PureWindowsPath(i).as_posix() for i in p0 if os.path.splitext(i)[1] in IMAGEFORMAT]
        p0 = lst
        for i, image_name in enumerate(p0):
            # print(f'{i}/{len(p0)} - {image_name}')
            if i % 5 == 0:
                val2017_lst.append('.'+ image_name[len(dir):])
            else:
                train2017_lst.append('.'+ image_name[len(dir):])
    with open(dir+'/train2017.txt', 'w', encoding='utf-8') as f:
        for l in train2017_lst:
            f.write(l+'\n')
    with open(dir+'/val2017.txt', 'w', encoding='utf-8') as f:
        for l in val2017_lst:
            f.write(l+'\n')
    print("create_train_val_txt Done.")
def create_train_txt():
    global dir, subdirs
    select = treeview.selection()
    train2017_lst, val2017_lst = [], []
    for i in select:
        subdir = treeview.item(i, "text")
        print(subdir)
        p0 = glob.glob(str(Path(subdir) / '**' / '*.*'), recursive=True)
        lst = [pathlib.PureWindowsPath(i).as_posix() for i in p0 if os.path.splitext(i)[1] in IMAGEFORMAT]
        p0 = lst
        for i, image_name in enumerate(p0):
            train2017_lst.append('.'+ image_name[len(dir):])
    with open(dir+'/train2017.txt', 'a', encoding='utf-8') as f:
        for l in train2017_lst:
            f.write(l+'\n')
    print("create_train_txt Done.")

import platform
if platform.system() == "Windows":
    root = Tk()
    root.geometry("900x600")
    dirpath = StringVar()
    Button(root, text='打开目录', command=opendir).pack() # 创建一个Button，点击弹出打开目录窗口
    Entry(root, textvariable=dirpath).pack(fill=X) # 创建Entry，显示选择的目录
    scrollbar = Scrollbar(root)
    scrollbar.pack(side=RIGHT, fill=Y)
    treeview = ttk.Treeview(root, yscrollcommand=scrollbar.set)
    treeview.pack(side=TOP, fill=BOTH, expand='yes')
    scrollbar.config(command=treeview.yview)
    treeview.config(yscrollcommand=scrollbar.set)
    Button(root, text='生成 train_val_txt', command=create_train_val_txt).pack(side=TOP) # 创建一个Button，点击弹出打开目录窗口
    Button(root, text='生成 train_txt', command=create_train_txt).pack(side=TOP) # 创建一个Button，点击弹出打开目录窗口
    root.mainloop()
else:
    p0 = glob.glob(str(Path('./') / '**' / '*.*'), recursive=True)
    lst = [i for i in p0 if os.path.splitext(i)[1] in IMAGEFORMAT]
    p0 = lst
    train2017_lst, val2017_lst = [], []
    for i, image_name in enumerate(p0):
        print(f'{i}/{len(p0)} - {image_name}')
        if i % 5 == 0:
            val2017_lst.append('./'+ image_name)
        else:
            train2017_lst.append('./'+ image_name)
    with open('train2017.txt', 'w', encoding='utf-8') as f:
        for l in train2017_lst:
            f.write(l+'\n')
    with open('val2017.txt', 'w', encoding='utf-8') as f:
        for l in val2017_lst:
            f.write(l+'\n')

