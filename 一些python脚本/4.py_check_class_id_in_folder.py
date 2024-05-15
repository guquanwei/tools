# -*- coding: utf-8 -*-
#
import argparse, io, copy, time, numpy, yaml, base64, re, os, glob, cv2, logging, shutil, pathlib
from PIL import Image, ImageDraw
import numpy as np
from pathlib import Path
import glob, skimage, cv2, os, shutil
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# from matplotlib.widgets import RectangleSelector
# # 支持中文
# plt.rcParams['font.sans-serif'] = ['SimSun']  # 用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
### v1.0
import ctypes, time, os
from functools import cmp_to_key
def find_files(path, postfix=None):
    files_list = []
    if postfix is not None:
        if not isinstance(postfix, list):
            postfix = [postfix]
        postfix = [x.lower() for x in postfix]
    for (root, sub_dirs, files) in os.walk(path):
        for file_name in files:
            if postfix is not None:
                file_postfix = os.path.splitext(file_name)
                if file_postfix[1].lower() not in postfix:
                    continue
            files_list.append(os.path.join(root, file_name).replace('\\', '/'))
        for sub_dir in sub_dirs:
            os.path.join(root, sub_dir)
    files_list.sort(key=cmp_to_key(ctypes.windll.shlwapi.StrCmpLogicalW))
    return files_list

def xywh2xyxy(xywh, w, h, s):
        return [float(xywh[0]-xywh[2]/2.0)*float(w)*s, float(xywh[1]-xywh[3]/2.0)*float(h)*s, \
               float(xywh[0]+xywh[2]/2.0)*float(w)*s, float(xywh[1]+xywh[3]/2.0)*float(h)*s]
def xyxy2xywh(xyxy, w, h, s):
        return [float(xyxy[0]/s+xyxy[2]/s)/2.0/float(w), float(xyxy[1]/s+xyxy[3]/s)/2.0/float(h), \
               float(xyxy[2]/s-xyxy[0]/s)/1.0/float(w), float(xyxy[3]/s-xyxy[1]/s)/1.0/float(h)]

def bbox_iou(xyxy1, xyxy2, h, w):
    """
    Compute the Intersection-Over-Union of a bounding box with respect to an array of other bounding boxes.

    Args:
        box1 (torch.Tensor): (4, )
        boxes (torch.Tensor): (n, 4)
        iou_thres (float): IoU threshold
        image_shape (tuple): (height, width)
        raw_output (bool): If True, return the raw IoU values instead of the indices

    Returns:
        high_iou_indices (torch.Tensor): Indices of boxes with IoU > thres
    """
    box1, box2 = xyxy1, xyxy2
    # Obtain coordinates for intersections
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    # Compute the area of intersection
    intersection = numpy.clip((x2 - x1), 0, w) * numpy.clip((y2 - y1), 0, h)

    # Compute the area of both individual boxes
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

    # Compute the area of union
    # union = box1_area + box2_area - intersection

    # Compute the IoU
    iou = intersection / box2_area  # Should be shape (n, )
    return iou
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
*********************************************************************************************************
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
IMAGEFORMAT = ['.jpg', '.jpeg', '.png', '.bmp',  '.cur', '.gif', '.ico', '.jfif', '.pcx', '.tiff', '.tga', '.webp', '.yuv']

# path = pathlib.PureWindowsPath(  r'C:\Users\pc\Desktop\person_car_gate'  ).as_posix()

"""
任意图像格式转化为cv2能正常读取的，可以顺利训练的
"""
# path = pathlib.PureWindowsPath(  r'E:\Project\2024\易县灾后城市管理项目\data_yixianzaihou1\223_Motor_vehicles_random_park_机动车乱停放_web'  ).as_posix()
# p0 = glob.glob(str(Path(path) / '**' / '*.*'), recursive=True)
# exts = []
# for i, image_name in enumerate(p0):
#     print(f'{i}/{len(p0)} - {image_name}')
#     if os.path.split(image_name)[1] == "classes.txt":
#         continue
#     ext = os.path.splitext(image_name)[1]
#     exts.append(ext)
#     if ext in [".xml", ".zip", ".txt", ".yaml", ".yml", ".pickle", ".tar", ".gz", ".rar", ".json"]:
#         continue
#     image = numpy.array(Image.open(image_name).convert('RGB'))
#     os.remove(image_name)
#     image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
#     cv2.imencode('.jpg', image)[1].tofile(os.path.splitext(image_name)[0]+'.jpg')
# print(list(set(exts)))

"""
文件批量重命名
"""
# p0 = glob.glob(str(Path(path) / '**' / '*.*'), recursive=True)
# for i, image_name in enumerate(p0):
#     print(f'{i}/{len(p0)} - {image_name}')
#     if os.path.split(image_name)[1] == "classes.txt":
#         continue
#     os.rename(image_name, os.path.split(image_name)[0]+'/smoking_gly_'+os.path.split(image_name)[1])

# import pathlib
# path = pathlib.Path(r'E:\Project\2024\data\登临项目-北京街镇-积水-占道经营-游商-垃圾-烟火-消防占道\zhandaojingying').as_posix()
# path_list = [p.as_posix() for p in pathlib.Path(path).glob("*") if pathlib.Path(p).is_dir()]
# path_list = path_list if len(path_list) > 0 else [path]
# for i, p in enumerate(path_list):
#     # print(p)
#     if p.find('exp') > 0:
#         continue
#     suffix_list = ['.jpg', '.png', '.txt']
#     file_list = [f.as_posix() for f in pathlib.Path(p).rglob("*") if pathlib.Path(f).is_file() and f.suffix.lower() in suffix_list]
#     pcids = []
#     for j, f in enumerate(file_list):
#         # print(f'{p} {i} - {f} {j}')
#         if os.path.split(f)[1] == "classes.txt":
#             continue
#         # os.rename(f, os.path.split(f)[0]+'/OccupyRoad'+os.path.split(f)[1])
#         os.rename(f, f.replace('OccupyRoad',''))
#         print(f"({j:4d} / {len(file_list):4d}) {f}")
#     print(f"\n({i:4d} / {len(path_list):4d}) {p}")
"""
删除txt没有对应的jpg
"""
# path = r'E:\Project\2024\data\吸烟玩手机检测\play_phone001'
# p0 = glob.glob(str(Path(path) / '**' / '*.jpg'), recursive=True)
# for i, q in enumerate(p0):
#     print(f'{i}/{len(p0)} - {q}')
#     if not os.path.exists(os.path.splitext(q)[0] + '.txt'):
#         os.remove(q)

# path = r'E:\Project\2024\data\吸烟检测\新建文件夹 - 2024-02-12\smoking3\person_head_hand_smoking_select'
# p0 = glob.glob(str(Path(path) / '*.*'))
# for i, q in enumerate(p0):
#     k = os.path.split(q)[1].split('.')[0].split('_')[-1]
#     if len(k) == 2:
#         print(f'{i}/{len(p0)} - {q}')
# #     label_name = os.path.splitext(q)[0] + '.txt'
# #     lines = []
# #     if not os.path.exists(label_name):
#         os.remove(q)

"""
补全每张jpg对应的txt, 补上空的txt
"""
# path = r'E:\Project\2024\生态环保\智慧工地\neg_sample'
# p0 = glob.glob(str(Path(path) / '**' / '*.jpg'), recursive=True)
# for i, q in enumerate(p0):
#     print(f'{i}/{len(p0)} - {q}')
#     label_name = os.path.splitext(q)[0] + '.txt'
#     lines2 = []
#     if not os.path.exists(label_name):
#         with open(label_name, 'w') as f:
#             for l in lines2:
#                 f.write(l+'\n')


"""""""""""""""""""""""""""""""""
查看labels的标签信息，修改class id
查看labels的标签信息，修改class id
查看labels的标签信息，修改class id
"""""""""""""""""""""""""""""""""

# import pathlib
# path = pathlib.Path(r'E:\Project\2024\登临项目-北京街镇-积水-占道经营-游商-垃圾-烟火-消防占道\jiezhen---2024-03-29-16').as_posix()
# path_list = [p.as_posix() for p in pathlib.Path(path).glob("*") if pathlib.Path(p).is_dir()]
# path_list = path_list if len(path_list) > 0 else [path]
# for i, p in enumerate(path_list):
#     # print(p)
#     if p.find('exp') > 0:
#         continue
#     suffix_list = ['.txt']
#     file_list = [f.as_posix() for f in pathlib.Path(p).rglob("*") if pathlib.Path(f).is_file() and f.suffix.lower() in suffix_list]
#     pcids = []
#     for j, f in enumerate(file_list):
#         # print(f'{p} {i} - {f} {j}')
#         if os.path.split(f)[1] == "classes.txt":
#             continue
#         lines, lines2, fcids = [], [], []
#         # image_name = os.path.splitext(f)[0]+'.jpg'
#         # if not os.path.exists(image_name):
#         #     image_name = os.path.splitext(f)[0]+'.png'
#         # img = cv2.imdecode(numpy.fromfile(image_name, dtype=numpy.uint8), cv2.IMREAD_COLOR)
#         # h, w = img.shape[0], img.shape[1]
#         with open(f, 'r', encoding='utf-8') as fn:
#             lines = [x.strip() for x in fn.read().strip().splitlines() if len(x.strip())]
#         for l in lines:
#             b = [float(x) for x in l.split(' ')]
#             cid, xywh = int(b[0]), b[1:5]
#             # xyxy = xywh2xyxy(xywh, w, h, 1)
#             # xyxy = [min(xyxy[0], xyxy[2]), min(xyxy[1], xyxy[3]), max(xyxy[0], xyxy[2]), max(xyxy[1], xyxy[3])]
#             # xyxy[0] = max(10, xyxy[0])
#             # xyxy[1] = max(10, xyxy[1])
#             # xyxy[2] = min(w-10, xyxy[2])
#             # xyxy[3] = min(h-10, xyxy[3])
#             # xywh = xyxy2xywh(xyxy, w, h, 1)
#             fcids.append(cid)
#             pcids.append(cid)
#             lines2.append('%d %.6f %.6f %.6f %.6f' % (cid, xywh[0], xywh[1], xywh[2], xywh[3]))
#         # print(f"({j:4d} / {len(file_list):4d}) {f} - {list(set(fcids))}")
#     print(f"\n({i:4d} / {len(path_list):4d}) {p} - ({len(file_list)}) - {list(set(pcids))}")

"""""""""""""""""""""""""""""""""
修改class id，!!! 谨慎使用，注意保存原始数据 ！！！
"""""""""""""""""""""""""""""""""

# import pathlib
# path = pathlib.Path(r'E:\Project\2024\登临项目-北京街镇-积水-占道经营-游商-垃圾-烟火-消防占道\jiezhen---2024-03-29-16\222_Off_store_占道经营_web2').as_posix()
# path_list = [p.as_posix() for p in pathlib.Path(path).glob("*") if pathlib.Path(p).is_dir()]
# path_list = path_list if len(path_list) > 0 else [path]
# for i, p in enumerate(path_list):
#     # print(p)
#     if p.find('exp') > 0:
#         continue
#     suffix_list = ['.txt']
#     file_list = [f.as_posix() for f in pathlib.Path(p).rglob("*") if pathlib.Path(f).is_file() and f.suffix.lower() in suffix_list]
#     pcids = []
#     for j, f in enumerate(file_list):
#         print(f'{p} {i} - {f} {j}')
#         if os.path.split(f)[1] == "classes.txt":
#             continue
#         image_name = os.path.splitext(f)[0]+'.jpg'
#         img = cv2.imdecode(numpy.fromfile(image_name, dtype=numpy.uint8), cv2.IMREAD_COLOR)
#         h, w = img.shape[0], img.shape[1]
#         lines, lines2, fcids = [], [], []
#         with open(f, 'r', encoding='utf-8') as fn:
#             lines = [x.strip() for x in fn.read().strip().splitlines() if len(x.strip())]
#         for l in lines:
#             if l[0] == '\x00':
#                 continue
#             b = [float(x) for x in l.split(' ')]
#             cid, xywh = int(b[0]), b[1:5]
#             # if cid == 222:
#             #     xyxy = xywh2xyxy(xywh, w, h, 1)
#             #     xyxy = [min(xyxy[0], xyxy[2]), min(xyxy[1], xyxy[3]), max(xyxy[0], xyxy[2]), max(xyxy[1], xyxy[3])]
#             #     # xyxy[0] = max(10, xyxy[0])
#             #     xyxy[1] = max(10, xyxy[1]-xyxy[3])
#             #     # xyxy[2] = min(w-10, xyxy[2])
#             #     # xyxy[3] = min(h-10, xyxy[3])
#             #     xywh = xyxy2xywh(xyxy, w, h, 1)
#             # if cid == 0:
#             # ddic = {0: 300, 1: 301, 2: 302, 3: 303, 4: 304, 5: 305, 6: 306}
#             # if cid == 0:
#             if cid > 10:
#                 fcids.append(cid)
#                 pcids.append(cid)
#                 lines2.append('%d %.6f %.6f %.6f %.6f' % (cid, xywh[0], xywh[1], xywh[2], xywh[3]))
#         lines2 = list(set(lines2))
#         with open(f, 'w') as fn:
#             for l in lines2:
#                 fn.write(l+'\n')
#         print(f"({j:4d} / {len(file_list):4d}) {f} - {list(set(fcids))}")
#     print(f"({i:4d} / {len(path_list):4d}) {p} - {list(set(pcids))}")




"""
把一个label拼入另一个
"""
# srcpath = r'E:\Project\2024\data\安全帽\helmet-v1.0.3\labels'
# dstpath = r'E:\Project\2024\data\安全帽\helmet-v1.0.3\qhewlmeetr'
# # p0 = glob.glob(str(Path(path) / '**' / '*.txt'), recursive=True) # dst
# p1 = glob.glob(str(Path(srcpath) / '**' / '*.txt'), recursive=True) # src
# for i, q in enumerate(p1):
#     if os.path.split(q)[1] == "classes.txt":
#         continue
#     if os.path.exists(q.replace('labels', 'qhewlmeetr')):
#         lines, lines2 = [], []
#         with open(q.replace('labels', 'qhewlmeetr'), 'r') as f:
#             lines = [x.strip() for x in f.read().strip().splitlines() if len(x.strip())]
#         with open(q, 'r') as f:
#             lines2 = [x.strip() for x in f.read().strip().splitlines() if len(x.strip())]
#         with open(q.replace('labels', 'qhewlmeetr'), 'w') as f:
#             for l in lines:
#                 f.write(l+'\n')
#             for l in lines2:
#                 f.write(l+'\n')
#     print(f'{i}/{len(p1)} - {q} ')


"""
根据label绘制标注结果，存到另外的地方
"""
# p1 = glob.glob(str(Path(path) / '**' / '*.*'), recursive=True)
# labels_clas_id, img_labels = [], []
# for i, image_name in enumerate(p1):
#     if os.path.split(image_name)[1] == "classes.txt" or os.path.splitext(image_name)[1] == '.txt':
#         continue
#     img_labels = []
#     lines, lines2 = [], []
#     label_name = os.path.splitext(image_name)[0] + '.txt'
#     img = cv2.imdecode(numpy.fromfile(image_name, dtype=numpy.uint8), cv2.IMREAD_COLOR)
#     h, w = img.shape[0], img.shape[1] 
#     with open(label_name, 'r') as f:
#         lines = [x.strip() for x in f.read().strip().splitlines() if len(x.strip())]
#     for l in lines:
#         b = [float(x) for x in l.split(' ')]
#         cid, cx, cy, cw, ch = int(b[0]), b[1], b[2], b[3], b[4]
#         x1, y1, x2, y2 = xywh2xyxy(b[1:5], w, h, 1)
#         label_size = (x2-x1)*(y2-y1)
#         img_labels.append(cid)
#         labels_clas_id.append(cid)
#         if label_size < 80:
#             cuted = img[int(y1):int(y2), int(x1):int(x2), :]
#             cuted_color =  numpy.mean(cuted)         
#             # cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color=(1, 255, 2), thickness=int(w*10/640.0))
#             # cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color=(1, 255, 2), thickness=1)
#             if cuted_color < 50:
#                 print(f'labels size is {(x2-x1)*(y2-y1)} ')
#                 # cv2.imencode('.jpg', cuted)[1].tofile('C:/Users/pc/Downloads/Crawler_Images/temp-001/' + os.path.split(image_name)[1])
#                 continue
#         lines2.append('%d %.6f %.6f %.6f %.6f' % (cid, cx, cy, cw, ch))
#     lines2 = list(set(lines2))
#     with open(label_name, 'w') as f:
#         for l in lines2:
#             f.write(l+'\n')
#     print(f'{i}/{len(p1)} - {image_name} - {list(set(img_labels))}')
# print(list(set(labels_clas_id)))


"""
把已有的图贴到大图中，生成新图，带上label信息
"""
# import random
# path1 = r'E:\Project\2024\data\吸烟玩手机检测\yihualu_smoking1_totrain\person_head_hand_smoking_select'
# p1 = glob.glob(str(Path(path1) / '**' / '*.jpg'), recursive=True)
# for i, q in enumerate(p1):
#     im0 = cv2.imdecode(numpy.fromfile(r'E:\Project\2024\data\吸烟玩手机检测\yihualu_smoking1_totrain\jiafang_smoking\smoke-1012.jpg', dtype=numpy.uint8), cv2.IMREAD_COLOR)
#     h0, w0 = im0.shape[0], im0.shape[1]
#     lines0 = []
#     with open(r'E:\Project\2024\data\吸烟玩手机检测\yihualu_smoking1_totrain\jiafang_smoking\smoke-1012.txt', 'r') as f:
#         lines0 = [x.strip() for x in f.read().strip().splitlines() if len(x.strip())]
#     for j in range(35, 101, 10):
#         coef = j / 100.0
#         im1 = cv2.imdecode(numpy.fromfile(q, dtype=numpy.uint8), cv2.IMREAD_UNCHANGED)
#         h1, w1 = im1.shape[0], im1.shape[1]
#         im2 = cv2.resize(im1, (int(im1.shape[1] * coef), int(im1.shape[0] * coef)))
#         h2, w2 = im2.shape[0], im2.shape[1]
#         if h2 >= h0 or w2 >= w0:
#             coef = max(1680/w2, 1000/h2)
#             im2 = cv2.resize(im2, (int(im2.shape[1] * coef), int(im2.shape[0] * coef)))
#             h2, w2 = im2.shape[0], im2.shape[1]
#         px, py = int(random.uniform(int(500), max(500, int(1500-w2)))),  int(random.uniform(int(200), max(200, int(600-h2))))
#         while( (py+h2) > 675 or (px+w2) > 1900 ):
#             coef *= 0.75
#             im2 = cv2.resize(im2, (int(im2.shape[1] * 0.75), int(im2.shape[0] * 0.75)))
#             h2, w2 = im2.shape[0], im2.shape[1]
#         lines, lines2 = [], []
#         with open(os.path.splitext(q)[0] + '.txt', 'r') as f:
#             lines = [x.strip() for x in f.read().strip().splitlines() if len(x.strip())]
#         for l in lines:
#             b = [float(x) for x in l.split(' ')]
#             cid, cx, cy, cw, ch = int(b[0]), b[1], b[2], b[3], b[4]
#             x1, y1, x2, y2 = xywh2xyxy(b[1:5], w1, h1, 1)
#             x1, y1, x2, y2 = x1 * coef, y1 * coef, x2 * coef, y2 * coef 
#             cx, cy, cw, ch = xyxy2xywh([x1+px, y1+py, x2+px, y2+py], w0, h0, 1)
#             lines2.append('%d %.6f %.6f %.6f %.6f' % (cid, cx, cy, cw, ch))
#         new_image = os.path.splitext(q.replace('person_head_hand_smoking_select', 'person_head_hand_smoking_select_anti'))[0] + f'_{int(coef*100)}.jpg'
#         new_label = os.path.splitext(q.replace('person_head_hand_smoking_select', 'person_head_hand_smoking_select_anti'))[0] + f'_{int(coef*100)}.txt'
#         with open(new_label, 'w') as f:
#             for l in lines0:
#                 f.write(l+'\n')
#         with open(new_label, 'a') as f:
#             for l in lines2:
#                 f.write(l+'\n')
#         print(f'{i}/{len(p1)} - {q}- {im0.shape} - {px} {py} {im2.shape}')
#         new_im = im0.copy()
#         new_im[py:py+h2, px:px+w2, :] = im2
#         # im0 = merge_img(im0, im2, py, py+im2.shape[0], px, px+im2.shape[1])
#         cv2.imencode('.jpg', new_im)[1].tofile(new_image)



"""
padding
"""
# import pathlib
# path = pathlib.PureWindowsPath( r'E:\Project\2024\data\吸烟检测\20240301\hand-smoking-4714-pad' ).as_posix()
# print(pathlib.Path(path).parent.as_posix())
# suffix_list = ['.jpg', '.jpeg', '.png', '.bmp',  '.cur', '.gif', '.ico', '.jfif', '.pcx', '.tiff', '.tga', '.webp', '.yuv']
# file_list = [f.as_posix() for f in pathlib.Path(path).rglob("*") if pathlib.Path(f).is_file and f.suffix.lower() in suffix_list]
# for i, image_file in enumerate(file_list):
#     print(f'{i}/{len(file_list)} - {image_file}')
#     image = cv2.imdecode(numpy.fromfile(image_file, dtype=numpy.uint8), cv2.IMREAD_COLOR)
#     shape = image.shape[:2]
#     h, w = image.shape[:2]
#     new_shape = (1080, 1920)
#     # Scale ratio (new / old)
#     r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
#     ratio = r, r  # width, height ratios
#     new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
#     dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
#     dw /= 2  # divide padding into 2 sides
#     dh /= 2
#     image = numpy.array(Image.fromarray(image).resize(new_unpad))
#     top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
#     left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
#     # im00 = numpy.zeros((5, 4, 3), dtype=numpy.uint8)
#     im1 = numpy.zeros((image.shape[0]+bottom+top, image.shape[1]+right+left, 3), dtype=numpy.uint8)
#     im1[top:top+image.shape[0], left:left+image.shape[1], :] = image
#     image = im1 # RGB 2 BGR
#     cv2.imencode('.jpg', image)[1].tofile(image_file)
#     lines, lines2 = [], []
#     with open(os.path.splitext(image_file)[0] + '.txt', 'r') as f:
#         lines = [x.strip() for x in f.read().strip().splitlines() if len(x.strip())]
#     for l in lines:
#         b = [float(x) for x in l.split(' ')]
#         cid = int(b[0])
#         x1, y1, x2, y2 = xywh2xyxy(b[1:5], w, h, 1)
#         cx, cy, cw, ch = xyxy2xywh([x1* r+left, y1* r+top, x2* r+left, y2* r+top], new_shape[1], new_shape[0], 1)
#         lines2.append('%d %.6f %.6f %.6f %.6f' % (cid, cx, cy, cw, ch))
#     with open(os.path.splitext(image_file)[0] + '.txt', 'w') as f:
#         for l in lines2:
#             f.write(l+'\n')



############# The End ###############
############# The End ###############
############# The End ###############