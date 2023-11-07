from os import walk
import os
from mp4parser import MP4
import os
import uuid
import re
import subprocess
import csv
import numpy as np



dirpath = '/home/ubuntu/data/h264_v20231107/'
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
for root, directories, filenames in os.walk(dirpath):
    for filename in filenames:

        path = os.path.join(root, filename)
        # print(path.encode('utf-8'))
        if path.endswith('.mp4'):

            uid = str(uuid.uuid4())
            
            #-frame_pts true: use the frame index for image names, otherwise, the index starts from 1 and increments 1 each time
            #cmd = f'ffmpeg -skip_frame nokey -i {path}  -vsync vfr -frame_pts true {imagepath}{uid}-%d.jpeg'
            #os.system(cmd)
            try:
                print('output',subprocess.check_output(['ffmpeg', '-skip_frame', 'nokey','-i', path,  '-vsync' ,'vfr', '-frame_pts', 'true', imagepath+uid+'-%d.jpeg']))
            except subprocess.CalledProcessError as err:
                print(err)


            #uid = '428a9041-ffa6-42d4-b2e0-b5df7f9c7978'
            iframe_index = []
            image_files = next(walk(imagepath), (None, None, []))[2]
            for frame_file in image_files:
                if frame_file.startswith(uid):
                    m = re.search(uid + '-' + '(\d+).jpeg', frame_file)
                    frame_idx = m.group(1)
                    iframe_index.append(int(frame_idx))


            mp4 = MP4(path)
            mp4.parse()
            frames = mp4.get_samples()
            iframe_files = []
            if frames is not None and len(frames):
                iframe_files = mp4.write_frame(path, [frames[i] for i in iframe_index],
                                               [uid + '-' + str(j) + '.h264' for j in iframe_index], h264path)


            for idx, iframe_file in enumerate(iframe_files):
                json_list.append({'h264': str(iframe_file), 'image': imagepath + image_files[idx], 'video': path})
            id_list +=  [uid + '-' + str(j) for j in iframe_index]

#with open("test.json", "w") as out_file:
#    json.dump(json_list, out_file, indent=6)


list_len = len(id_list)
np.random.shuffle(id_list)
trainlist, validlist, testlist = np.split(id_list, 
                       [int(.8*list_len), int(.9*list_len)])
with open(dirpath + "dataset.csv",  mode='w') as f:

        writer = csv.writer(f)
        writer.writerow(['id','flag'])
        for row in trainlist:
            writer.writerow([row,'TRAIN'])
        for row in validlist:
            writer.writerow([row,'VALIDATE'])
        for row in testlist:
            writer.writerow([row,'TEST'])

