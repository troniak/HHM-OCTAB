import sys
import time
from matplotlib import pyplot as plt
from numpy import *
import numexpr as ne
from lib.agreement_metrics import *
from lib.utils import *
from lib.io_utils import *
import scipy.io as sio
import os
import shutil
output_headers = [] #global parameter (defined below)

fps = 25 #framerate of target_video
inputs = sys.argv #MTurk output containing all annotations for target_video
target_video = inputs[1] #filename of target_video (without extension)
target_min_time = 180.0 #denote video seconds of interest (from which to extract annotations)
target_max_time = 210.0
target_min_frame = int(round(fps*target_min_time)) #denote video frames of interest
target_max_frame = int(round(fps*target_max_time))
target_num_frames = target_max_frame - target_min_frame
baseFrame   = int(round(fps*(target_min_time)))

def rowval(row,key): #convenience macro
  return row[output_headers.index(key)]

#instantiate output matrices
annotation_matrix = zeros(shape=(target_num_frames,target_num_frames))
tag_matrix = zeros(shape=(target_num_frames,target_num_frames), dtype=np.object)

output_name = inputs[2]
csvreader = init_csv(output_name,'rbU')
rowsIter = iter(csvreader)

#pre-read all rows
output_headers = next(rowsIter) #first row of file is the header
rowsA = [[]];
for rows in rowsIter:
  rowsA += [rows]

for rowA in rowsA:
  if(len(rowA) > 0): #non-empty row

#get data from mturk output file
    video_name   = url2name(rowval(rowA,'Input.video_url_webm'))
    if(video_name == target_video):# if data re: video we are interested in
      startTimes   = ([float(time_str) for time_str in strip_first(rowval(rowA,'Answer.startTimeList'),'|','0').split('|')])
      endTimes     = ([float(time_str) for time_str in strip_first(rowval(rowA,'Answer.endTimeList'),'|','0').split('|')])
      tags         = ([tag for tag in strip_first(rowval(rowA,'Answer.annotationText'),'|').split('|')])
      vid_start_time= float(rowval(rowA,'Input.start_time'))

#populate annotation matrix and tag matrix from the data
      for startTime,endTime,tag in zip(startTimes, endTimes, tags):
        startFrame  = int(round(fps*(vid_start_time + startTime)))
        endFrame    = int(round(fps*(vid_start_time + endTime)))-1
        #print 'time : %f, %f, %s' % (vid_start_time+startTime, vid_start_time+endTime, tag) #debug
        #print 'frame: %d, %d, %s' % (startFrame, endFrame, tag) #debug
        if(startFrame >= target_min_frame and endFrame <= target_max_frame):
          rr = startFrame - baseFrame #convert frames to matrix indices
          cc = endFrame - baseFrame
          print 'indices: %d, %d, %s' % (rr, cc, tag) #debug
          #add 1 for each time a worker annotates an action with this startFrame and endFrame
          annotation_matrix[rr,cc] += 1
          #concatenate all tags given to action annotated at this startFrame and endFrame
          tag_matrix[rr,cc] = str(tag_matrix[rr,cc])+tag+";"

#save annotation and tag matrices (with optional report)
#print 'video ' + target_video + ' @ time %.0f:' %target_min_time
sio.savemat('annotation_matrix.mat', {'annotation_matrix':annotation_matrix, 'tag_matrix':tag_matrix})
