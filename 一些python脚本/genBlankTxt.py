import os

path = "D:\shuju\pa\新村\holdUmbrella"
for file in os.listdir(path):
    if file[-4:]==".jpg":
       file_name = file[:-4]
       file_txt = file_name + ".txt"
       file_txtpath = os.path.join(path, file_txt)
       if not os.path.exists(file_txtpath):
           with open(file_txtpath,"w") as f:
               print(file_txtpath)
