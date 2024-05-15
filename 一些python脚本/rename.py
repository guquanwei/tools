import os
path = 'D:\shuju\pa\新村\suitcase'
files = os.listdir(path)
for file in files:
    if file=="classes.txt":
        continue
    os.rename(os.path.join(path,file),os.path.join(path,"suitcase"+file))