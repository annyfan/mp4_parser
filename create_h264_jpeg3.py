from os import walk
import os

from mp4parser import MP4
import os
import uuid
import re
import subprocess
import csv
import numpy as np

videopath = "/data/h264_v20230221/h264"
dirpath = '/data/h264_v20231126/'
resolution = '64x64'
h264dir = 'h264/'
imagedir = 'image/'

tmpdir = 'temp/'

h264path = os.path.join(dirpath, h264dir)
isExist = os.path.exists(h264path)
if not isExist:
    os.makedirs(h264path)

imagepath = os.path.join(dirpath, imagedir)
isExist = os.path.exists(imagepath)
if not isExist:
    os.makedirs(imagepath)


temppath = os.path.join(dirpath, tmpdir)
isExist = os.path.exists(temppath)
if not isExist:
    os.makedirs(temppath)

dirpath = os.path.expanduser(dirpath)
json_list = []
id_list = []
    

json_list = []
id_list = []
for filename in  os.listdir(videopath):
    fpath = os.path.join(videopath, filename)
    # print(path.encode('utf-8'))
    
    if fpath.endswith('.h264'):
        name = filename.removesuffix(".h264")
        out_h264 =  os.path.join(dirpath, h264dir, filename)
        out_image = os.path.join(dirpath, imagedir, name + ".jpeg")
        tmp_h264 = os.path.join(temppath, filename)
        try:
            if resolution is not None:
                print(f'begin converting h264:{out_h264}')
                print('output',subprocess.check_output(['ffmpeg', '-i', fpath,   '-vf', 'scale=' + resolution, tmp_h264]))
                print('end converting h264')
                MP4.convert_h264_data(tmp_h264, out_h264)
                print('output',subprocess.check_output(['ffmpeg', '-framerate', '25', '-i', tmp_h264,   '-frames:v', '1', out_image]))
                
            else: 
                MP4.convert_h264_data(fpath, out_h264)
                print('output',subprocess.check_output(['ffmpeg', '-framerate', '25', '-i', out_h264,   '-frames:v', '1', out_image]))
            
        except OSError:
            pass
        except subprocess.CalledProcessError as err:
            print(err) 

for filename in  os.listdir(temppath):
    fpath = os.path.join(temppath, filename)
    # print(path.encode('utf-8'))
    if fpath.endswith('.h264'):
        try:
            #print(fpath)
            os.remove(fpath)
        except OSError:
             pass
os.rmdir(temppath) 

