from os import walk
import os
from mp4parser import MP4
import os
import uuid
import re
import subprocess
import csv
import numpy as np
from os import listdir


dirpath = '/data/h264_v20231121/'


dirpath = os.path.expanduser(dirpath)
json_list = []
id_list = []
for filename in  listdir(dirpath):
    fpath = os.path.join(dirpath, filename)
    # print(path.encode('utf-8'))
    if fpath.endswith('.h264'):
        try:
            #print(fpath)
            os.remove(fpath)
        except OSError:
             pass
            