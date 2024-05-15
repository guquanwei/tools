import cv2

def run(image):
    im_draw = image.copy()
    im_disp = image.copy()
    window_name = "Select objects to be tracked here"
    cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
    cv2.imshow(window_name,im_draw)

    run.mouse_down = False
    pts_1=[]
    pts_2=[]

    def callback(event,x,y,flags,param):
        if event== cv2.EVENT_LBUTTONDOWN:
            run.mouse_down = True
            pts_1.append((x, y))
        elif event == cv2.EVENT_LBUTTONUP and run.mouse_down == True:
            run.mouse_down = False
            pts_2.append((x, y))
            print("Object selected at [{},{}]".format(pts_1[-1], pts_2[-1]))
        elif event == cv2.EVENT_MOUSEMOVE and run.mouse_down == True:
            im_draw = image.copy()
            cv2.rectangle(im_draw, pts_1[-1], (x, y), (255, 255, 255), 3)
            cv2.imshow(window_name, im_draw)

    print("Press and release mouse around the project to be tracked")
    cv2.setMouseCallback(window_name,callback)

    print("Press key 'p' to continue with the selected points")


    window_name_2 = "Object to be tracked"

    while True:
        if(pts_1!=[] and pts_2!=[]):
            cv2.rectangle(im_disp,pts_1[-1],pts_2[-1],(255,255,255),3)
        cv2.namedWindow(window_name_2,cv2.WINDOW_NORMAL)
        cv2.imshow(window_name_2,im_disp)
        if(cv2.waitKey(20)&0xff==ord('p')):
            box = pts_1[-1]+pts_2[-1]
            box = checkPoint(box)
            cv2.destroyAllWindows()
            # print("1")
            break
        # else:
        #     print("Input Error")
        #     exit()
    return box
def checkPoint(box):
    if box[2]>box[0]:
        max_x = box[2]
        min_x = box[0]
    else:
        max_x = box[2]
        min_x = box[0]
    if box[3]>box[1]:
        max_y = box[3]
        min_y = box[1]
    else:
        max_y = box[1]
        min_y = box[3]
    return (min_x,min_y,max_x,max_y)








