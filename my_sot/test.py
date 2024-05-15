# import cv2
#
# def run(source):
#     cam = cv2.VideoCapture(source)
#
#     cv2.namedWindow("frame",cv2.WINDOW_NORMAL)
#     cv2.namedWindow("frame2", cv2.WINDOW_NORMAL)
#     # while True:
#     #     retval,frame = cam.read()
#     #     cv2.imshow("frame",frame)
#     #     cv2.waitKey(20)
#
#     retval, frame = cam.read()
#     cv2.imshow("frame2", frame)
#     cv2.imshow("frame",frame)
#     while True:
#         cv2.waitKey(20)
#
#
# if __name__ == "__main__":
#     run("docs/demo/demo-video-single.avi")


tinydict = {('name','sd'): 'Zara', 'Age': 7}

print("tinydict['Name']: ", tinydict[('name','sd')])

import time
localtime = time.localtime(time.time())
# localtime = time.asctime(localtime)
localtime = time.strftime("%Y-%m-%d %H:%M:%S",localtime)
print(localtime)