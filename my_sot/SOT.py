import cv2
import dlib
import get_points


def xyxy2xywh(xyxy, w, h, s):
    return [float(xyxy[0] / s + xyxy[2] / s) / 2.0 / float(w), float(xyxy[1] / s + xyxy[3] / s) / 2.0 / float(h), \
            float(xyxy[2] / s - xyxy[0] / s) / 1.0 / float(w), float(xyxy[3] / s - xyxy[1] / s) / 1.0 / float(h)]

def run(source):
    num=1
    cid = 96

    cam = cv2.VideoCapture(source)
    if not(cam.isOpened):
        print("Video device or file couldn't be opened")
        exit()
    print("Press key 'p' to pause the video to start tracking")
    while True:
        retval,image = cam.read()
        if not retval:
            print("Cannot capture frame")
            exit()
        cv2.namedWindow("Image",cv2.WINDOW_NORMAL)
        cv2.imshow("Image",image)
        if(cv2.waitKey(20)&0xff==ord('p')):
            break
    cv2.destroyWindow("Image")

    box = get_points.run(image)

    if not box:
        print("No object to track")
        exit()

    cv2.namedWindow("Image",cv2.WINDOW_NORMAL)
    cv2.imshow("Image",image)

    tracker = dlib.correlation_tracker()
    tracker.start_track(image,dlib.rectangle(box[0],box[1],box[2],box[3]))

    while True:
        retval, image = cam.read()
        if not retval:
            print("Cannot capture frame device | CODE TERMINATING :(")
            exit()
        # Update the tracker
        tracker.update(image)
        # Get the position of the object, draw a
        # bounding box around it and display it.
        rect = tracker.get_position()
        pt1 = (int(rect.left()), int(rect.top()))
        pt2 = (int(rect.right()), int(rect.bottom()))

        h = image.shape[0]
        w = image.shape[1]
        box = xyxy2xywh((pt1[0], pt1[1], pt2[0], pt2[1]), w, h, 1)

        cv2.imwrite("./Pics/" + f"{num}.jpg", image)
        with open("./Labels/" + f"{num}.txt","w") as f:
            f.write(f"{cid} {box[0]} {box[1]} {box[2]} {box[3]}\n")

        cv2.rectangle(image, pt1, pt2, (255, 255, 255), 3)
        print("Object tracked at [{}, {}] \r".format(pt1, pt2))


        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.imshow("Image", image)
        cv2.waitKey(20)
        # if cv2.waitKey(20)&0xff == ord('q'):
        #     break

        num+=1
    cam.release()

if __name__ == "__main__":
    source = "docs/demo/2.mp4"
    run(source)



