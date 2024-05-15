import cv2 as cv
import os


def image_to_video():
    file_path = r'D:\shuju\pa\yixian\images\images'  # 图片目录
    output = 'D:\shuju\pa\yixian\de_1_2.mp4'  # 生成视频路径
    img_list = sorted(os.listdir(file_path)) # 生成图片目录下以图片名字为内容的列表
    height = 1080
    weight = 1920
    fps = 24
    # fourcc = cv.VideoWriter_fourcc('M', 'J', 'P', 'G') 用于avi格式的生成
    fourcc = cv.VideoWriter_fourcc(*'mp4v')  # 用于mp4格式的生成
    videowriter = cv.VideoWriter(output, fourcc, fps, (weight, height))  # 创建一个写入视频对象
    for i in range(852):
        path = file_path + r"\frame" + str(i) + ".jpg"
        if(not os.path.exists(path)):
            continue
        print(path)
        frame = cv.imread(path)
        videowriter.write(frame)

    videowriter.release()


image_to_video()
