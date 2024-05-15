# -*- coding: utf-8 -*-
# 
from PIL import Image, ImageTk
import tkinter, yaml
import ctypes, time, os, pathlib
from functools import cmp_to_key
def find_files(path, postfix=None): ### v1.0.0
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
class Colors: # Ultralytics color palette https://ultralytics.com/
    def __init__(self):
        # hex = matplotlib.colors.TABLEAU_COLORS.values()
        hexs = ('FF3838', 'FF9D97', 'FF701F', 'FFB21D', 'CFD231', '48F90A', '92CC17', '3DDB86', '1A9334', '00D4BB',
                '2C99A8', '00C2FF', '344593', '6473FF', '0018EC', '8438FF', '520085', 'CB38FF', 'FF95C8', 'FF37C7')
        self.palette = [f'#{c}' for c in hexs]
        self.n = len(self.palette)
    def __call__(self, i, bgr=False):
        c = self.palette[int(i) % self.n]
        return c
class ImageLabeler(tkinter.Frame):
    """ an image view canvas to display and label bbox on the images. """
    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.geometry("900x600")
        with open('E:/Dataset/zkdn_ai.yaml', encoding='utf-8') as f:
            d = yaml.safe_load(f)
        self.names       = d["names"]
        self.colors      = Colors() #{0: '#FF3030', 61: '#FF3030', 140: '#00FFFF', 141: "#7FFF00", 142: '#00FFFF', 147: '#FF3030', 150: "#7FFF00", 95: '#0000FF', 96: '#0000FF', 126: '#7FFF00', 127: '#7F6600', 221: '#FF3030', 222: '#7FFF00', 218: '#7FFF00'} ###
        self.menu_items  = [f"{i} - {self.names[i]}" for i in [0, 1, 2, 3, 5, 7, 147, 154, 200, 221, 222, 230]]
        self.menu_items.append("delete")
        

        """ set images_labels path """
        path = pathlib.PureWindowsPath(  r'F:\exp9'  ).as_posix() ### ********* 'set images_labels path' ********* ###
        """ set images_labels path """

        
        self.image_index = 0  ### set image index
        self.class_id    = 221
        self.color       = '#FF3030'
        self.imagelist   = find_files(path, ['.mp4', '.jpg', '.jpeg', '.png', '.bmp',   '.cur', '.gif', '.ico', '.jfif', '.pcx', '.tiff', '.tga', '.webp', '.yuv'])
        """ Initialize bbox variable. """
        self.bboxes      = {}
        self.bbox_id     = None
        self.x0          = 0
        self.y0          = 0
        self.cursors     = {0: "sizing", 1: "sb_v_double_arrow", 2: "sizing", 3: "sb_h_double_arrow", 4: "sizing", 5: "sb_v_double_arrow", 6: "sizing", 7: "sb_h_double_arrow", 8: "fleur", 9: "arrow"}
        self.R           = 6 # circle radius at rectangle corner
        self.LButtonPressed = False
        self.isdirty     = False
        """ Initialize UI elements. """
        self.parent.title("v1.1.0")
        self.canvas = tkinter.Canvas(self.parent, bg='gray')
        self.canvas.pack(side='right', fill='both', expand='yes')
        self.parent.update()
        self.image = None
        self.scale = 1.0
        self.imgsz = None
        self.photo = tkinter.PhotoImage()
        self.imagecontainer = self.canvas.create_image((0, 0), image=self.photo, anchor='nw')
        if len(self.imagelist) > 0:
            self.image = Image.open(self.imagelist[self.image_index])
            self.scale = min(float(self.canvas.winfo_height())/float(self.image.height), float(self.canvas.winfo_width())/float(self.image.width))
            self.imgsz = self.image.resize((int(self.image.width*self.scale), int(self.image.height*self.scale)))
            self.photo = ImageTk.PhotoImage(image=self.imgsz)
            self.canvas.itemconfig(self.imagecontainer, image=self.photo)
        """ create pop menu """
        self.menu = tkinter.Menu(self.parent, tearoff=False)
        for i in range(len(self.menu_items)):
            self.menu.add_command(label=self.menu_items[i], command=lambda msg=self.menu_items[i]: self.menu_callback(msg=msg))
        """ bind mouse event """
        self.canvas.bind("<Button-1>",        self.onLeftButtonPress)
        self.canvas.bind("<ButtonRelease-1>", self.onLeftButtonRelease)
        self.canvas.bind("<Button-3>",        self.onRightButtonPress)
        self.canvas.bind("<Motion>",          self.onMotion)
        self.canvas.bind("<MouseWheel>",      self.onMouseWheel)
        self.parent.bind("<Key>",             self.onKeyPress)

    def get_closest_bbox(self, event):
        closest_bbox = None
        marker       = 9
        min_distance = float('inf')
        for bbox_id, v in self.bboxes.items():
            l, t, r, b = v["xyxy"]
            x1, y1, x2, y2 = min(l, r), min(t, b), max(l, r), max(t, b)
            distance = min(min((event.x - x1 - self.R*2), (x2 - self.R*2 - event.x)), min((event.y - y1 - self.R*2), (y2 - self.R*2 - event.y)))
            if 0 < distance < min_distance:
                closest_bbox = bbox_id
                marker       = 8
                min_distance = distance
            for i in range(8):
                if i == 0:
                    distance = ((x1 - event.x) ** 2 + (y1 - event.y) ** 2) ** 0.5
                if i == 1:
                    x, y = (l + r)/2, t
                    distance = abs(y1 - event.y) if x1 + self.R < event.x < x2 - self.R else float('inf')
                if i == 2:
                    distance = ((x2 - event.x) ** 2 + (y1 - event.y) ** 2) ** 0.5
                if i == 3:
                    x, y = r, (t + b)/2
                    distance = abs(x2 - event.x) if y1 + self.R < event.y < y2 - self.R else float('inf')
                if i == 4:
                    distance = ((x2 - event.x) ** 2 + (y2 - event.y) ** 2) ** 0.5
                if i == 5:
                    x, y = (l + r)/2, b
                    distance = abs(y2 - event.y) if x1 + self.R < event.x < x2 - self.R else float('inf')
                if i == 6:
                    distance = ((x1 - event.x) ** 2 + (y2 - event.y) ** 2) ** 0.5
                if i == 7:
                    x, y = l, (t + b)/2
                    distance = abs(x1 - event.x) if y1 + self.R < event.y < y2 - self.R else float('inf')
                if 0 < distance < min_distance and distance < self.R*2:
                    closest_bbox = bbox_id
                    marker       = i
                    min_distance = distance
        return closest_bbox, marker

    def onLeftButtonPress(self, event):
        self.x0, self.y0 = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.LButtonPressed = True
        closest_bbox, marker = self.get_closest_bbox(event)
        if closest_bbox is None:
            self.bbox_id = None
            for k, v in self.bboxes.items():
                self.bboxes[k]["focus"] = 0
        else:
            self.bbox_id = closest_bbox
            self.class_id = self.bboxes[self.bbox_id]["class_id"]
            x1, y1, x2, y2 = self.bboxes[self.bbox_id]["xyxy"]
            self.bboxes[self.bbox_id]["xyxy"] = [min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)]
            for k, v in self.bboxes.items():
                self.bboxes[k]["focus"] = 0
            self.bboxes[self.bbox_id]["focus"]  = 1
            self.bboxes[self.bbox_id]["marker"] = marker
        for bbox_id, v in self.bboxes.items():
            for k in ["NW", "N", "NE", "E", "SE", "S", "SW", "W"]:
                self.canvas.delete(self.bboxes[bbox_id][k])
            if self.bboxes[bbox_id]["focus"] >= 1:
                x1, y1, x2, y2 = v["xyxy"]
                color = self.colors(self.class_id)
                for k, v in zip(["NW", "NE", "SE", "SW"], [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]):
                    l, t, r, b = v[0] - self.R, v[1] - self.R, v[0] + self.R, v[1] + self.R
                    self.bboxes[bbox_id][k] = self.canvas.create_oval(l, t, r, b, fill=color, outline=color, width=self.R-3)
                for k, v in zip(["N", "E", "S", "W"], [[(x1+x2)/2, y1], [x2, (y1+y2)/2], [(x1+x2)/2, y2], [x1, (y1+y2)/2]]):
                    l, t, r, b = v[0] - self.R, v[1] - self.R, v[0] + self.R, v[1] + self.R
                    self.bboxes[bbox_id][k] = self.canvas.create_rectangle(l, t, r, b, fill=color, outline=color, width=self.R-3)
        event.widget.config(cursor=self.cursors[marker])
        if len(self.imagelist):
            self.parent.title(f"{self.image_index+1}/{len(self.imagelist)} {self.imagelist[self.image_index]}")
    
    def add_bbox(self, cid, x1, y1, x2, y2, focus):
        # self.class_id = cid
        color = self.colors(cid)
        self.bbox_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=self.R-3)
        self.bboxes[self.bbox_id] = {"class_id": cid, "xyxy": [x1, y1, x2, y2], "focus": focus, "text": None, "textbg": None, "marker": 4, "NW": None, "N": None, "NE": None, "E": None, "SE": None, "S": None, "SW": None, "W": None, "log": []}
        self.bboxes[self.bbox_id]["text"] = self.canvas.create_text(x1, y1, text=f"{cid} - {self.names[cid]}", anchor='sw', font=("Purisa", self.R*3), fill=color, tag="text")
        l, t, r, b = self.canvas.bbox(self.bboxes[self.bbox_id]["text"])
        anchor = 'se' if r > self.imgsz.width else 'nw' if t < 0 else 'sw'
        self.canvas.itemconfig(self.bboxes[self.bbox_id]["text"], anchor=anchor)
        l, t, r, b = self.canvas.bbox(self.bboxes[self.bbox_id]["text"])
        self.bboxes[self.bbox_id]["textbg"] = self.canvas.create_rectangle(l+1, t, r, b, fill=color, outline=color, width=self.R-3)
        self.canvas.itemconfig(self.bboxes[self.bbox_id]["text"], fill="white")
        self.canvas.tag_raise("text")
        if focus == 1:
            x1, y1, x2, y2 = self.bboxes[self.bbox_id]["xyxy"]
            for k, v in zip(["NW", "NE", "SE", "SW"], [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]):
                l, t, r, b = v[0] - self.R, v[1] - self.R, v[0] + self.R, v[1] + self.R
                self.bboxes[self.bbox_id][k] = self.canvas.create_oval(l, t, r, b, fill=color, outline=color, width=self.R-3)
            for k, v in zip(["N", "E", "S", "W"], [[(x1+x2)/2, y1], [x2, (y1+y2)/2], [(x1+x2)/2, y2], [x1, (y1+y2)/2]]):
                l, t, r, b = v[0] - self.R, v[1] - self.R, v[0] + self.R, v[1] + self.R
                self.bboxes[self.bbox_id][k] = self.canvas.create_rectangle(l, t, r, b, fill=color, outline=color, width=self.R-3)
    
    def onMotion(self, event):
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        if self.LButtonPressed:
            if self.bbox_id is None: # create
                self.add_bbox(self.class_id, self.x0, self.y0, x, y, 1)
            else: # movable or resizable
                x1, y1, x2, y2 = self.bboxes[self.bbox_id]["xyxy"]
                marker = self.bboxes[self.bbox_id]["marker"]
                if marker == 0:
                    x1, y1, x2, y2 = x, y, x2, y2
                if marker == 1:
                    x1, y1, x2, y2 = x1, y, x2, y2
                if marker == 2:
                    x1, y1, x2, y2 = x1, y, x, y2
                if marker == 3:
                    x1, y1, x2, y2 = x1, y1, x, y2
                if marker == 4:
                    x1, y1, x2, y2 = x1, y1, x, y
                if marker == 5:
                    x1, y1, x2, y2 = x1, y1, x2, y
                if marker == 6:
                    x1, y1, x2, y2 = x, y1, x2, y
                if marker == 7:
                    x1, y1, x2, y2 = x, y1, x2, y2
                if marker == 8:
                    delta_x, delta_y = x - self.x0, y - self.y0
                    x1, y1, x2, y2 = x1 + delta_x, y1 + delta_y, x2 + delta_x, y2 + delta_y
                    self.x0, self.y0 = x, y
                self.bboxes[self.bbox_id]["xyxy"] = [x1, y1, x2, y2] # save coords
                self.canvas.coords(self.bbox_id, x1, y1, x2, y2)
                self.canvas.coords(self.bboxes[self.bbox_id]["text"], x1+1, y1)
                l, t, r, b = self.canvas.bbox(self.bboxes[self.bbox_id]["text"])
                self.canvas.coords(self.bboxes[self.bbox_id]["textbg"], l+1, t, r, b)
                for k, v in zip(["NW", "NE", "SE", "SW",  "N", "E", "S", "W"], [[x1, y1], [x2, y1], [x2, y2], [x1, y2],
                                [(x1+x2)/2, y1], [x2, (y1+y2)/2], [(x1+x2)/2, y2], [x1, (y1+y2)/2]]):
                    l, t, r, b = v[0] - self.R, v[1] - self.R, v[0] + self.R, v[1] + self.R
                    self.canvas.coords(self.bboxes[self.bbox_id][k], l, t, r, b)
                self.isdirty = True
        else:
            closest_bbox, marker = self.get_closest_bbox(event)
            event.widget.config(cursor=self.cursors[marker])
            for bbox_id, v in self.bboxes.items():
                if bbox_id == closest_bbox:
                    self.canvas.itemconfig(bbox_id, width=self.R-3, dash=(100, 3))
                else:
                    self.canvas.itemconfig(bbox_id, width=self.R-3, dash=())

        if len(self.imagelist):
            self.parent.title(f"{self.image_index+1}/{len(self.imagelist)} {self.imagelist[self.image_index]}")

    def onLeftButtonRelease(self, event):
        # x = self.canvas.canvasx(event.x)
        # y = self.canvas.canvasy(event.y)
        self.LButtonPressed = False

    def onRightButtonPress(self, event):
        self.x0, self.y0 = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        closest_bbox, marker = self.get_closest_bbox(event)
        if closest_bbox is None:
            self.bbox_id = None
            for k, v in self.bboxes.items():
                self.bboxes[k]["focus"] = 0
        else:
            self.bbox_id = closest_bbox
            self.class_id = self.bboxes[self.bbox_id]["class_id"]
            x1, y1, x2, y2 = self.bboxes[self.bbox_id]["xyxy"]
            self.bboxes[self.bbox_id]["xyxy"] = [min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)]
            for k, v in self.bboxes.items():
                self.bboxes[k]["focus"] = 0
            self.bboxes[self.bbox_id]["focus"]  = 1
            self.bboxes[self.bbox_id]["marker"] = marker
        for bbox_id, v in self.bboxes.items():
            for k in ["NW", "N", "NE", "E", "SE", "S", "SW", "W"]:
                self.canvas.delete(self.bboxes[bbox_id][k])
            if self.bboxes[bbox_id]["focus"] >= 1:
                x1, y1, x2, y2 = v["xyxy"]
                color = self.colors(self.class_id)
                for k, v in zip(["NW", "NE", "SE", "SW"], [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]):
                    l, t, r, b = v[0] - self.R, v[1] - self.R, v[0] + self.R, v[1] + self.R
                    self.bboxes[bbox_id][k] = self.canvas.create_oval(l, t, r, b, fill=color, outline=color, width=self.R-3)
                for k, v in zip(["N", "E", "S", "W"], [[(x1+x2)/2, y1], [x2, (y1+y2)/2], [(x1+x2)/2, y2], [x1, (y1+y2)/2]]):
                    l, t, r, b = v[0] - self.R, v[1] - self.R, v[0] + self.R, v[1] + self.R
                    self.bboxes[bbox_id][k] = self.canvas.create_rectangle(l, t, r, b, fill=color, outline=color, width=self.R-3)
        event.widget.config(cursor=self.cursors[marker])
        
        self.menu.post(event.x_root,  event.y_root)

    def menu_callback(self, msg):
        print(f'click menu : {msg}')
        if msg == "delete":
            for k in ["NW", "N", "NE", "E", "SE", "S", "SW", "W"]:
                self.canvas.delete(self.bboxes[self.bbox_id][k])
            self.canvas.delete(self.bboxes[self.bbox_id]["textbg"])
            self.canvas.delete(self.bboxes[self.bbox_id]["text"])
            self.canvas.delete(self.bbox_id)
            del self.bboxes[self.bbox_id]
            self.bbox_id = None
        else:
            if 0 <= int(msg.split(' ')[0]) <= 365 and self.bbox_id is not None:
                self.class_id = int(msg.split(' ')[0])
                self.bboxes[self.bbox_id]["class_id"] = self.class_id
                color = self.colors(self.class_id)
                self.canvas.itemconfig(self.bbox_id, outline=color)
                self.canvas.itemconfig(self.bboxes[self.bbox_id]["textbg"], fill=color, outline=color)
                self.canvas.itemconfig(self.bboxes[self.bbox_id]["text"], text=f"{self.class_id} - {self.names[self.class_id]}")
                x1, y1, x2, y2 = self.bboxes[self.bbox_id]["xyxy"]
                for k, v in zip(["NW", "NE", "SE", "SW"], [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]):
                    l, t, r, b = v[0] - self.R, v[1] - self.R, v[0] + self.R, v[1] + self.R
                    self.canvas.itemconfig(self.bboxes[self.bbox_id][k], fill=color, outline=color)
                for k, v in zip(["N", "E", "S", "W"], [[(x1+x2)/2, y1], [x2, (y1+y2)/2], [(x1+x2)/2, y2], [x1, (y1+y2)/2]]):
                    l, t, r, b = v[0] - self.R, v[1] - self.R, v[0] + self.R, v[1] + self.R
                    self.canvas.itemconfig(self.bboxes[self.bbox_id][k], fill=color, outline=color)
                self.canvas.tag_raise("text")
        self.isdirty = True

    def onMouseWheel(self, event):
        """Set final rectangle coords.
        Binds to <ButtonRelease-3> event."""
        """ Save last label """
        if self.isdirty == True:
            self.isdirty = False
            lines = []
            for k, v in self.bboxes.items():
                xyxy = v["xyxy"]
                xyxy = [min(xyxy[0], xyxy[2]), min(xyxy[1], xyxy[3]), max(xyxy[0], xyxy[2]), max(xyxy[1], xyxy[3])]
                xyxy[0] = max(10, xyxy[0])
                xyxy[1] = max(10, xyxy[1])
                xyxy[2] = min(self.imgsz.width-10, xyxy[2])
                xyxy[3] = min(self.imgsz.height-10, xyxy[3])
                x, y, w, h = self.xyxy2xywh(xyxy, self.image.width, self.image.height, self.scale)
                lines.append('%d %.6f %.6f %.6f %.6f' % (int(v["class_id"]), x, y, w, h))
            image = self.imagelist[self.image_index]
            label = os.path.splitext(image)[0] + '.txt'
            if not os.path.exists(label):
                if not os.path.exists(os.path.split(label)[0]):
                    os.makedirs(os.path.split(label)[0])
            with open(label, 'w+') as f: ### 全量重写
                for l in lines:
                    f.write(l+'\n')
        """ respond to Linux or Windows wheel event """
        if event.num == 4 or event.delta == 120:  ### up
            self.image_index = 0 if self.image_index - 1 < 0 else self.image_index - 1
        if event.num == 5 or event.delta == -120: ### down
            self.image_index = len(self.imagelist) - 1 if self.image_index + 1 >= len(self.imagelist) else self.image_index + 1
        for item in self.canvas.find_all():
            if item > 1:
                self.canvas.delete(item)
        self.bboxes = {}
        """ load image """
        if len(self.imagelist) > 0:
            self.image = Image.open(self.imagelist[self.image_index])
            self.scale = min(float(self.canvas.winfo_height())/float(self.image.height), float(self.canvas.winfo_width())/float(self.image.width))
            self.imgsz = self.image.resize((int(self.image.width*self.scale), int(self.image.height*self.scale)))
            self.photo = ImageTk.PhotoImage(image=self.imgsz)
            self.canvas.itemconfig(self.imagecontainer, image=self.photo)
            """ load label bbox """
            self.isdirty = False
            image = self.imagelist[self.image_index]
            label = os.path.splitext(image)[0] + '.txt'
            if os.path.exists(label):
                lines = []
                with open(label, 'r') as f:
                    lines = [x.strip() for x in f.read().strip().splitlines() if len(x.strip())]
                for l in lines:
                    v = [float(x) for x in l.split(' ')]
                    x1, y1, x2, y2 = self.xywh2xyxy(v[1:5], self.image.width, self.image.height, self.scale)
                    self.add_bbox(int(v[0]), x1, y1, x2, y2, 0)
                    self.isdirty = True if (x1 > x2) or (y1 > y2) else False
            self.parent.title(f"{self.image_index+1}/{len(self.imagelist)} {self.imagelist[self.image_index]}")

    def xyxy2xywh(self, xyxy, w, h, s):
        return [float(xyxy[0]/s+xyxy[2]/s)/2.0/float(w), float(xyxy[1]/s+xyxy[3]/s)/2.0/float(h), \
               float(xyxy[2]/s-xyxy[0]/s)/1.0/float(w), float(xyxy[3]/s-xyxy[1]/s)/1.0/float(h)]

    def xywh2xyxy(self, xywh, w, h, s):
        return [float(xywh[0]-xywh[2]/2.0)*float(w)*s, float(xywh[1]-xywh[3]/2.0)*float(h)*s, \
               float(xywh[0]+xywh[2]/2.0)*float(w)*s, float(xywh[1]+xywh[3]/2.0)*float(h)*s]

    def onKeyPress(self, event):
        if event.char == 'c':
            print('press c delete this bbox')
            pass

if __name__ == '__main__':
    root = tkinter.Tk()
    ImageLabeler(root)
    root.mainloop()



# class Handle():
#     def __init__(self, name, pos) -> None:
#         super().__init__()
#         self._name = name
#         self._pos = pos
# class item():
#     def __init__(self,x0, y0, x1, y1) -> None:
#         super().__init__()
#         self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
#         self._handles = [Handle("nw", (x0, y0)),
#                          Handle("n",  ((x0+x1)/2, y0)), 
#                          Handle("ne", (x1, y0)), 
#                          Handle("e",  (x1, (y0+y1)/2)),
#                          Handle("se", (x1, y1)), 
#                          Handle("s",  ((x0+x1)/2, y1)),
#                          Handle("sw", (x0, y1)),
#                          Handle("w",  (x1, (y0+y1)/2))]
# def get_closest_bbox_handle_at_point(items, x, y, d=6):
#     """Look for a handle at ``pos`` and return the tuple (item, handle)."""
#     def find(item):
#         """Find item's handle at pos."""
#         for h in item._handles:
#             if -d < (h._pos[0] - x) < d and -d < (h._pos[1] - y) < d:
#                 return h
#     for item in items:
#         h = find(item)
#         if h:
#             return item, h._name
#     return None, None

# items = [item(10,10,110,110), item(60,60,160,160)]
# item, h = get_closest_bbox_handle_at_point(items, 115, 115, d=6)
# print(h)