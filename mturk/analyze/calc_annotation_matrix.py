import sys
import time
from matplotlib import pyplot as plt
from numpy import *
import numexpr as ne
from agreement_metrics import *
from utils import *
from io_utils import *
import scipy.io as sio
import os
import shutil
output_headers = []
#videos = [      'bike','bike','bike', '50salad', '50salad','50salad', 'cmu_salad', 'cmu_salad', 'cmu_salad','pbj','pbj','pbj','tum','tum','tum']#,'julia']
videos = ['pbj','pbj','pbj','pbj','pbj','pbj','pbj','pbj','pbj','pbj','pbj','pbj','pbj']
#start_times = [ 0.0,10.0,20.0,           180.0,190.0,200.0,               120.0,130.0,140.0,                   2.0,12.0,22.0,    15.0,25.0,35.0]
start_times = [0.0,2.5,5.0,7.5,10.0,12.5,15.0,17.5,20.0,22.5,25.0,27.5,30.0]
fps = 25
vid_len = 40
inputs = sys.argv
target_video = 'pbj'
target_start_time = 0#180.0

def rowval(row,key):
  return row[output_headers.index(key)]

#for target_video,target_start_time in zip(videos,start_times):
for a in [1]:
  annotation_matrix = zeros(shape=(fps*vid_len,fps*vid_len))
  tag_matrix = zeros(shape=(fps*vid_len,fps*vid_len), dtype=np.object)#, itemsize=256)
  output_name = inputs[1]
  if(os.path.isfile('/Users/troniak/Downloads/'+output_name+'.csv')):
    shutil.move('/Users/troniak/Downloads/'+output_name+'.csv', '../output/'+output_name+'.csv')
  csvreader = init_csv('../output/'+output_name,'rb')
  rowsIter = iter(csvreader)
  output_headers = next(rowsIter)
  #print output_headers
  rowsA = [[]]
  rowsB = [[]]
  count = 0
  for rows in rowsIter:
    rowsA += [rows]
    rowsB += [rows]
  for rowA in rowsA:
    if(len(rowA) > 0):
      startTimes   = ([float(time_str) for time_str in strip_first(rowval(rowA,'Answer.startTimeList'),'|','0').split('|')])
      endTimes     = ([float(time_str) for time_str in strip_first(rowval(rowA,'Answer.endTimeList'),'|','0').split('|')])
      tags         = ([tag for tag in strip_first(rowval(rowA,'Answer.annotationText'),'|').split('|')])
      video_name   = url2name(rowval(rowA,'Input.video_url_webm'))
      vid_start_time= float(rowval(rowA,'Input.start_time'))
      if(video_name == target_video):
        #print video_name
        for startTime,endTime,tag in zip(startTimes, endTimes, tags):
          print '%f, %f' % (fps*vid_start_time + fps*startTime, fps*vid_start_time + fps*endTime)
          #annotation_matrix[startTime,endTime] += 1
          annotation_matrix[fps*vid_start_time + fps*startTime, fps*vid_start_time + fps*endTime] += 1
          tag_matrix[fps*vid_start_time + fps*startTime, fps*vid_start_time + fps*endTime] = tag


  print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
  print 'results for video ' + target_video + ' @ time %.0f:' %target_start_time
  #print '\tnumber of matches: %d' % len(eam)
  #print curr_aam
  #print 'start frames %f, %f, %f' % (180*fps,190*fps,200*fps)
  #plt.imshow(annotation_matrix)
  #plt.show()
  #print annotation_matrix
  #first_frame = 180 * 25;
  #last_frame = 210 * 25;
  #sio.savemat('annotation_matrix.mat', {'annotation_matrix':annotation_matrix[first_frame:last_frame,first_frame:last_frame], 'tag_matrix':tag_matrix[first_frame:last_frame,first_frame:last_frame]})
  sio.savemat('annotation_matrix.mat', {'annotation_matrix':annotation_matrix, 'tag_matrix':tag_matrix})
  print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
