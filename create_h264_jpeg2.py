from os import listdir, walk
import os
from mp4parser import MP4
import os
import uuid
import re
import subprocess
import csv
import numpy as np



dirpath = '/data/h264_v20231121/'
h264dir = 'h264/'
imagedir = 'image/'

h264path = os.path.join(dirpath, h264dir)
isExist = os.path.exists(h264path)
if not isExist:
    os.makedirs(h264path)
imagepath = os.path.join(dirpath, imagedir)
isExist = os.path.exists(imagepath)
if not isExist:
    os.makedirs(imagepath)

dirpath = os.path.expanduser(dirpath)
json_list = []
id_list = []
for filename in  listdir(dirpath):
    path = os.path.join(dirpath, filename)
        # print(path.encode('utf-8'))
    if path.endswith('.mp4'):

        #uid = str(uuid.uuid4())
        uid = '428a9041-ffa6-42d4-b2e0-b5df7f9c7978'
            
        #ffmpeg -i 20230114_ApexLegends_faide.mp4 -vf "scale=910x512" 20230114_ApexLegends_faide.mp4
            
        # it should be 0 based but It becomes 1 based in 1 test. 
        #ffmpeg -skip_frame nokey -i 20230114_ApexLegends_faide_512.mp4  -vsync vfr -frame_pts true 428a9041-ffa6-42d4-b2e0-b5df7f9c7978-%d.jpeg
        #cmd = f'ffmpeg -skip_frame nokey -i {path}  -vsync vfr -frame_pts true {imagepath}{uid}-%d.jpeg'
        #os.system(cmd)

        # 1based
        #ffmpeg -i 20230114_ApexLegends_faide_512.mp4  -f image2  -vcodec copy  -bsf h264_mp4toannexb "%d.h264" 
        cmd = f'ffmpeg -i {path} -f image2  -vcodec copy  -bsf h264_mp4toannexb "%d.h264"'
        os.system(cmd)
  

           
        iframe_index = []
        image_files = next(walk(imagepath), (None, None, []))[2]
        print(len(image_files))
        for frame_file in image_files:
            if frame_file.startswith(uid):
                m = re.search(uid + '-' + '(\d+).jpeg', frame_file)
                frame_idx = m.group(1)
                iframe_index.append(int(frame_idx))
                id_list.append( uid + '-' + str(frame_idx))



        iframe_files = []
        add_one_based = 1 if 0 in iframe_index else 0
        if iframe_index is not None and len(iframe_index):
            for j in iframe_index:
                    
                cmd = f'mv {dirpath}{j + add_one_based}.h264 {h264path}{uid}-{j}.h264'
                os.system(cmd)


list_len = len(id_list)
print(list_len)
np.random.shuffle(id_list)
trainlist, validlist, testlist = np.split(id_list, 
                       [int(.8*list_len), int(.9*list_len)])

if os.path.exists('dataset.csv'):
    os.remove('dataset.csv')

with open(dirpath + "dataset.csv",  mode='w') as f:

        writer = csv.writer(f)
        writer.writerow(['id','flag'])
        for row in trainlist:
            writer.writerow([row,'TRAIN'])
        for row in validlist:
            writer.writerow([row,'VALIDATE'])
        for row in testlist:
            writer.writerow([row,'TEST'])

