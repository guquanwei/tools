import os
import shutil
targetpath = r'D:\shuju\pa\新村\data\data'
path = r'D:\shuju\pa\新村\data\data\222_Off_store_店外经营_haidian_0504_100'

for filename in os.listdir(path):
    if filename[-4:]==".txt":
        file_path = os.path.join(path, filename)
        if filename=="classes":
            continue
        with open(file_path,'r') as f:
            print(file_path)
            anns = f.readlines()
            if len(anns)==0:
                if (os.path.exists(os.path.join(path, filename[:-4] + ".jpg"))):
                    shutil.copyfile(file_path, os.path.join(targetpath+r"\0",filename))
                    shutil.copyfile(os.path.join(path, filename[:-4] + ".jpg"), os.path.join(targetpath+r"\0", filename[:-4] + ".jpg"))
            else:
                cid = anns[0].split(" ")[0]
                if cid=='221':
                    if (os.path.exists(os.path.join(path, filename[:-4] + ".jpg"))):
                        shutil.copyfile(file_path, os.path.join(targetpath + r"\221", filename))
                        shutil.copyfile(os.path.join(path, filename[:-4] + ".jpg"),os.path.join(targetpath+r"\221", filename[:-4] + ".jpg"))
                if cid=='222':
                    if (os.path.exists(os.path.join(path, filename[:-4] + ".jpg"))):
                        shutil.copyfile(file_path, os.path.join(targetpath + r"\222", filename))
                        shutil.copyfile(os.path.join(path, filename[:-4] + ".jpg"),os.path.join(targetpath+r"\222", filename[:-4] + ".jpg"))