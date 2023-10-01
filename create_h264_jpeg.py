import json
from os import walk
import mp4parser
import os
import sys
import io
from mp4parser import MP4
import os
import uuid
import re
import subprocess

dirpath = '/content/drive/MyDrive/internship/byteNet/'
h264dir = 'vh264/'
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

            #uid = 'b37fbfd2-83f3-4281-ab36-6be70bc118c0'
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

with open("test.json", "w") as out_file:
    json.dump(json_list, out_file, indent=6)
