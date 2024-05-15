import argparse, io, copy, time, numpy, base64, re, glob, cv2, os, shutil
from PIL import Image, ImageDraw
import numpy as np
from pathlib import Path
import random


def xywh2xyxy(xywh, w, h, s):
    return [float(xywh[0] - xywh[2] / 2.0) * float(w) * s, float(xywh[1] - xywh[3] / 2.0) * float(h) * s, \
            float(xywh[0] + xywh[2] / 2.0) * float(w) * s, float(xywh[1] + xywh[3] / 2.0) * float(h) * s]


def xyxy2xywh(xyxy, w, h, s):
    return [float(xyxy[0] / s + xyxy[2] / s) / 2.0 / float(w), float(xyxy[1] / s + xyxy[3] / s) / 2.0 / float(h), \
            float(xyxy[2] / s - xyxy[0] / s) / 1.0 / float(w), float(xyxy[3] / s - xyxy[1] / s) / 1.0 / float(h)]


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

path2= r'./高空抛物/抠图'
path1 = r'./高空抛物/大楼图片挑选'
louPaths = glob.glob(str(Path(path1) /'*.jpg'), recursive=True)
objectPaths = glob.glob(str(Path(path2) /'*.png'), recursive=True)

savePath = r'./高空抛物/合成图片'
num=1765

for object_i, obiect in enumerate(objectPaths):
    for lou_i,lou in enumerate(louPaths):

        coef = 0.5

        # 打开背景图片和要贴上去的图片
        bg_img = Image.open(lou)
        bg_imgWidth, bg_imgHeight = bg_img.size

        overlay_img = Image.open(obiect)
        overlay_imgWidth, overlay_imgHeight = overlay_img.size

        # 将要贴上去的图片缩放尺寸
        overlay_img = overlay_img.resize((int(overlay_imgWidth*coef),int(overlay_imgHeight*coef)))
        overlay_imgWidth, overlay_imgHeight = overlay_img.size

        px, py = int(random.uniform(int(bg_imgWidth*0.25), int(bg_imgWidth*0.75))), int(
            random.uniform(int(bg_imgHeight*0.25), int(bg_imgHeight*0.75)))
        # print(1)
        while ((overlay_imgHeight*overlay_imgWidth>0.004*bg_imgHeight*bg_imgWidth) or (py + overlay_imgHeight) > bg_imgHeight or (px + overlay_imgWidth) > bg_imgWidth) :
            coef *= 0.75
            overlay_imgHeight = int(overlay_imgHeight * coef)
            overlay_imgWidth = int(overlay_imgWidth * coef)
            overlay_img = overlay_img.resize((overlay_imgWidth, overlay_imgHeight))

            # im2 = cv2.resize(overlay_img, (int(im2.shape[1] * 0.75), int(im2.shape[0] * 0.75)))
            # h2, w2 = im2.shape[0], im2.shape[1]
            overlay_imgWidth, overlay_imgHeight = overlay_img.size


        # 将要贴上去的图片贴到背景图片上
        bg_img.paste(overlay_img, (px , py ), overlay_img)

        txtPath = os.path.join(savePath, f"high_row{num}.txt")
        with open(txtPath, 'w') as f:
            cid = 148
            box = xyxy2xywh((px,py,px+overlay_imgWidth,py+overlay_imgHeight),bg_imgWidth,bg_imgHeight,1)
            f.write(f"{cid} {box[0]} {box[1]} {box[2]} {box[3]}\n")
        # 保存结果图片
        bg_img.save(os.path.join(savePath,f"high_row{num}.png"))
        print(savePath+f"high_row{num}.png")
        num+=1