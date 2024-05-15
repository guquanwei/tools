# -*- coding: utf-8 -*-
#
import argparse, io, copy, time, numpy, base64, re, glob, cv2, os, shutil
from PIL import Image, ImageDraw
import numpy as np
from pathlib import Path



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

path = r'E:\Project\2024\data\吸烟检测\新建文件夹 - 2024-02-12\smoking3\person_head_hand_with_smoking - 副本'


"""
查看labels的标签信息，修改class id
查看labels的标签信息，修改class id
"""
p1 = glob.glob(str(Path(path) / '**' / '*.txt'), recursive=True)
for i, q in enumerate(p1):
    if os.path.split(q)[1] == "classes.txt":
        continue
    image_name = os.path.splitext(q)[0]+'.jpg'
    img = cv2.imdecode(numpy.fromfile(image_name, dtype=numpy.uint8), cv2.IMREAD_COLOR)
    h, w = img.shape[0], img.shape[1]
    cids, lines, lines2, lines3 = [], [], [], []
    with open(q, 'r') as f:
        lines = [x.strip() for x in f.read().strip().splitlines() if len(x.strip())]
    for l in lines:
        b = [float(x) for x in l.split(' ')]
        cid, xywh = int(b[0]), b[1:5]
        xyxy = xywh2xyxy(xywh, w, h, 1)
        xyxy[0] = max(10, xyxy[0])
        xyxy[1] = max(10, xyxy[1])
        xyxy[2] = min(w-10, xyxy[2])
        xyxy[3] = min(h-10, xyxy[3])
        xywh = xyxy2xywh(xyxy, w, h, 1)
        cids.append(cid)
        lines2.append('%d %.6f %.6f %.6f %.6f' % (cid, xywh[0], xywh[1], xywh[2], xywh[3]))
    lines2 = list(set(lines2))
    with open(q, 'w') as f:
        for l in lines2:
            f.write(l+'\n')
    print(f'{i}/{len(p1)} - {q} - {list(set(cids))}')




"""
把已有的图贴到大图中，生成新图，带上label信息
"""
import random
path1 = r'E:\Project\2024\data\吸烟检测\新建文件夹 - 2024-02-12\smoking3\person_head_hand_smoking_select'
p1 = glob.glob(str(Path(path1) / '**' / '*.jpg'), recursive=True)
for i, q in enumerate(p1):
    im0 = cv2.imdecode(numpy.fromfile(r'E:\Project\2024\data\吸烟检测\新建文件夹 - 2024-02-12\smoking3\jiafang_smoking\smoke-1012.jpg', dtype=numpy.uint8), cv2.IMREAD_COLOR)
    h0, w0 = im0.shape[0], im0.shape[1]
    lines0 = []
    with open(r'E:\Project\2024\data\吸烟检测\新建文件夹 - 2024-02-12\smoking3\jiafang_smoking\smoke-1012.txt', 'r') as f:
        lines0 = [x.strip() for x in f.read().strip().splitlines() if len(x.strip())]
    for j in range(35, 101, 10):
        coef = j / 100.0
        im1 = cv2.imdecode(numpy.fromfile(q, dtype=numpy.uint8), cv2.IMREAD_UNCHANGED)
        h1, w1 = im1.shape[0], im1.shape[1]
        im2 = cv2.resize(im1, (int(im1.shape[1] * coef), int(im1.shape[0] * coef)))
        h2, w2 = im2.shape[0], im2.shape[1]
        if h2 >= h0 or w2 >= w0:
            coef = max(1680/w2, 1000/h2)
            im2 = cv2.resize(im2, (int(im2.shape[1] * coef), int(im2.shape[0] * coef)))
            h2, w2 = im2.shape[0], im2.shape[1]
        px, py = int(random.uniform(int(500), max(500, int(1500-w2)))),  int(random.uniform(int(200), max(200, int(600-h2))))
        while( (py+h2) > 675 or (px+w2) > 1900 ):
            coef *= 0.75
            im2 = cv2.resize(im2, (int(im2.shape[1] * 0.75), int(im2.shape[0] * 0.75)))
            h2, w2 = im2.shape[0], im2.shape[1]
        lines, lines2 = [], []
        with open(os.path.splitext(q)[0] + '.txt', 'r') as f:
            lines = [x.strip() for x in f.read().strip().splitlines() if len(x.strip())]
        for l in lines:
            b = [float(x) for x in l.split(' ')]
            cid, cx, cy, cw, ch = int(b[0]), b[1], b[2], b[3], b[4]
            x1, y1, x2, y2 = xywh2xyxy(b[1:5], w1, h1, 1)
            x1, y1, x2, y2 = x1 * coef, y1 * coef, x2 * coef, y2 * coef 
            cx, cy, cw, ch = xyxy2xywh([x1+px, y1+py, x2+px, y2+py], w0, h0, 1)
            lines2.append('%d %.6f %.6f %.6f %.6f' % (cid, cx, cy, cw, ch))
        new_image = os.path.splitext(q.replace('person_head_hand_smoking_select', 'person_head_hand_smoking_select_anti'))[0] + f'_{int(coef*100)}.jpg'
        new_label = os.path.splitext(q.replace('person_head_hand_smoking_select', 'person_head_hand_smoking_select_anti'))[0] + f'_{int(coef*100)}.txt'
        with open(new_label, 'w') as f:
            for l in lines0:
                f.write(l+'\n')
        with open(new_label, 'a') as f:
            for l in lines2:
                f.write(l+'\n')
        print(f'{i}/{len(p1)} - {q}- {im0.shape} - {px} {py} {im2.shape}')
        new_im = im0.copy()
        new_im[py:py+h2, px:px+w2, :] = im2
        # im0 = merge_img(im0, im2, py, py+im2.shape[0], px, px+im2.shape[1])
        cv2.imencode('.jpg', new_im)[1].tofile(new_image)




############# The End ###############
############# The End ###############
############# The End ###############