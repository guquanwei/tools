# -*- coding:utf-8 -*-
# 

import pathlib, cv2
# path = pathlib.Path(r'E:\Dataset\zkdn_person_mobilebike_car_truck\video3').as_posix()
# path_list = [p.as_posix() for p in pathlib.Path(path).glob("*") if pathlib.Path(p).is_dir()]
# path_list = path_list if len(path_list) > 0 else [path]
# for i, p in enumerate(path_list):
#     suffix_list = ['.mp4']
#     file_list = [f.as_posix() for f in pathlib.Path(p).rglob("*") if pathlib.Path(f).is_file() and f.suffix.lower() in suffix_list]
#     for j, f in enumerate(file_list):

path = r'E:\Project\2024\易县灾后城市管理项目\演示视频'
file_list = 'a'
j = 0
f = r'E:\Project\2024\易县灾后城市管理项目\演示视频\de_1_2.mp4'

capture = cv2.VideoCapture(f)

width       = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
height      = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps         = int(capture.get(cv2.CAP_PROP_FPS))
frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

fps         = int(fps) if fps is not None and 0.1 < fps < 120 else int(20)
fps         = 1
frame_id    = 0

while (frame_id >= 0) :
    ret, frame = capture.read()
    if ret:
        if frame_id % fps == 0:
            cv2.imencode('.jpg', frame)[1].tofile(f'{path}/{pathlib.Path(f).name[:-4]}_{frame_id}.jpg')
            print(f"{frame_id} {frame_count} Get the image data id is {frame_id}")
        frame_id += 1
    else:
        break
capture.release()





# import cv2, numpy

# source = r'E:\Project\2024\易县灾后城市管理项目\data\t_register_202112020500_02_事件_05_街面秩序_0506_非机动车乱停放_050601_非机动车乱停放_7__IMGTH.jpg'
# frame = cv2.imdecode(numpy.fromfile(source, dtype=numpy.uint8), cv2.IMREAD_COLOR)

# frame_width, frame_height = frame.shape[1], frame.shape[0]
# fps, fourcc = int(25), cv2.VideoWriter_fourcc(*'mp4v')

# # Output setup
# video_writer = cv2.VideoWriter(r'E:\output-2024-04-08.mp4', fourcc, fps, (frame_width, frame_height))

# vid_frame_count = 0

# # Iterate over video frames
# while True:
#     # success, frame = videocapture.read()
#     # if not success:
#     #     break
    
#     vid_frame_count += 1
#     # frame = frame[...,::-1]
#     cv2.imshow('', frame)

#     video_writer.write(frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# video_writer.release()
# # videocapture.release()
# cv2.destroyAllWindows()



# source = r'E:\Project\2024\易县灾后城市管理项目\data\t_register_202112020500_02_事件_05_街面秩序_0506_非机动车乱停放_050601_非机动车乱停放_7__IMGTH.jpg'

# # Video setup
# videocapture = cv2.VideoCapture(source)
# frame_width, frame_height = int(videocapture.get(3)), int(videocapture.get(4))
# fps, fourcc = int(videocapture.get(5)), cv2.VideoWriter_fourcc(*'mp4v')

# # Output setup
# video_writer = cv2.VideoWriter(r'C:\Users\pc\Downloads\1470663151-1-192-output-cut.mp4', fourcc, fps, (frame_width, frame_height))

# vid_frame_count = 0

# # Iterate over video frames
# while videocapture.isOpened():
#     success, frame = videocapture.read()
#     if not success:
#         break
#     vid_frame_count += 1
#     frame = frame[...,::-1]
#     cv2.imshow('Ultralytics YOLOv8 Region Counter Movable', frame)

#     video_writer.write(frame)

#     # if vid_frame_count > fps*5:
#     #     break

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# video_writer.release()
# videocapture.release()
# cv2.destroyAllWindows()
 