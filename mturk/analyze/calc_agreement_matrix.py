import sys
import time
from matplotlib import pyplot as plt
from numpy import *
import numexpr as ne
from agreement_metrics import *
from utils import *
from io_utils import *
output_headers = []
videos = [      'bike','bike','bike', '50salad', '50salad','50salad', 'cmu_salad', 'cmu_salad', 'cmu_salad','pbj','pbj','pbj','tum','tum','tum']#,'julia']
start_times = [ 0.0,10.0,20.0,           180.0,190.0,200.0,               120.0,130.0,140.0,                   2.0,12.0,22.0,    15.0,25.0,35.0]
fps = 25
vid_len = 220
inputs = sys.argv
target_video = '50salad'
target_start_time = 0#180.0

def rowval(row,key):
  return row[output_headers.index(key)]

#for target_video,target_start_time in zip(videos,start_times):
for a in [1]:
  curr_aam = zeros(shape=(fps*vid_len,fps*vid_len))
  output_name = inputs[1]
  csvreader = init_csv('../output/'+output_name,'rb')
  rowsIter = iter(csvreader)
  output_headers = next(rowsIter)
  rowsA = [[]]
  rowsB = [[]]
  count = 0
  for rows in rowsIter:
    rowsA += [rows]
    rowsB += [rows]
  for rowA in rowsA:
  #for b in [1]:
    if(len(rowA) > 0):
      #plt.imshow(curr_aam)
      #plt.show()
    #if(1):
      try:
        startTimesA   = ([float(time_str) for time_str in strip_first(rowval(rowA,'Answer.startTimeList'),'|').split('|')])
        endTimesA     = ([float(time_str) for time_str in strip_first(rowval(rowA,'Answer.endTimeList'),'|').split('|')])
        vid_start_time= float(rowval(rowA,'Input.start_time'))
        #print '.',
        for rowB in rowsB:
          if(len(rowB) > 0):
            try:
              startTimesB   = ([float(time_str) for time_str in strip_first(rowval(rowB,'Answer.startTimeList'),'|').split('|')])
              endTimesB     = ([float(time_str) for time_str in strip_first(rowval(rowB,'Answer.endTimeList'),'|').split('|')])
              if(len(startTimesA) > 0 and len(startTimesB) > 0): #at least one annotation was made
                if(rowval(rowA,'WorkerId') != rowval(rowB,'WorkerId')): #don't compare worker against self in same video
                #if(1):
                  #if(1):
                  #print url2name(rowval(rowA,'Input.video_url_webm'))
                  if(url2name(rowval(rowA,'Input.video_url_webm')) == target_video):
                    #print size(curr_aam)
                    #print 'between ' + rowval(rowA,'WorkerId') + ' and ' + rowval(rowB,'WorkerId')
                    tmp = calc_annotation_agreement(startTimesA,endTimesA,startTimesB,endTimesB,5,fps,vid_len,vid_start_time)
                    #time1 = time.time()
                    #curr_aam = ne.evaluate("curr_aam + tmp")
                    if(tmp != None):
                      curr_aam += tmp
                    #time2 = time.time()
                    #print 'function took %0.3f ms' % ((time2-time1)*1000.0)
                    #plt.imshow(curr_aam)
                    #plt.show()
                    #print curr_aam
            except ValueError:
              a=1
              #print 'Hit ' + rowval(rowB,'HITId') + ' contains no annotations!'
      except ValueError:
        a=1
        #print 'Hit ' + rowval(rowA,'HITId') + ' contains no annotations!'

  print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
  print 'results for video ' + target_video + ' @ time %.0f:' %target_start_time
  #print '\tnumber of matches: %d' % len(eam)
  #print curr_aam
  plt.imshow(curr_aam)
  plt.show()
  print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
