import csv
import sys
import re
from numpy import arange
from numpy import divide
from numpy import array
import numpy as np
import os
import shutil
from matplotlib import pyplot as plt
import itertools
import boto.mturk.connection as conn
import boto.mturk.qualification as qual
from agreement_metrics import *
from utils import *
from io_utils import *


mturk = conn.MTurkConnection(aws_access_key_id='AKIAJUL53VTH3ENYMNIQ', aws_secret_access_key='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', is_secure=True, port=None, proxy=None, proxy_port=None, proxy_user=None, proxy_pass=None, host=None, debug=0, https_connection_factory=None, security_token=None, profile_name=None)

headers = ['video_url_mp4', 'video_url_webm','title','start_time','end_time']
output_headers = []
url = 'http://cs.ubc.ca/~troniak/'
template_name = 'template.html'
action_annotation_type_id = '276M25L8I9N3M15OL9FEFQW7T8OIS7'
videos = [      'bike','bike','bike', '50salad', '50salad','50salad', 'cmu_salad', 'cmu_salad', 'cmu_salad','pbj','pbj','pbj','tum','tum','tum']#,'julia']
start_times = [ 0.0,10.0,20.0,           180.0,190.0,200.0,               120.0,130.0,140.0,                   2.0,12.0,22.0,    15.0,25.0,35.0]
inputs = sys.argv
time_diff_sum = 0
time_diff_count = 0
wordcounts = {} #counts frequency of words within all annotations
segcounts  = {} #counts # segments per video
vidcounts  = {} #counts # times video was annotated
vid_time_diff = {} #sum of difference between start and end times by video
vid_time_count = {} #count of start time differences
annotation_tracker = [] #tracks annotations by video
delta_counter = 0.1
delta_y_counter = 0.01
counter = delta_counter
y_counter = delta_y_counter

def increment_wordcounts(annotationArr):
  for annotation in annotationArr:
    words = annotation.split()
    for word in words:
      if(wordcounts.has_key(word)):
        wordcounts[word] = wordcounts[word] + 1
      else:
        wordcounts[word] = 1

def rowval(row,key):
  return row[output_headers.index(key)]

for target_video,target_start_time in zip(videos,start_times):
  output_name = inputs[1]
#target_video = inputs[2]#'bike'
#target_start_time = float(inputs[3])#0.0+0
  csvreader = init_csv('../output/'+output_name,'rb')
#sortedlist = sorted(csvreader, key=operator.itemgetter(3), reverse=True)
#hitId workerId status mp4Filename webmFilename videoStartTimeStr videoEndTime #noMoreAction
#videoTitlesStrB  = strip_first(rowB[output_headers.index('Answer.annotationText')],'|')
  rowsIter = iter(csvreader)
  output_headers = next(rowsIter)
  rowsA = [[]]
  rowsB = [[]]

  alp = [] #track krippendorf alpha measurements
  eam = [] #track event agreement measurements
  sam = [] #track segmentation agreement measurements

  for rows in rowsIter:
    rowsA += [rows]
    rowsB += [rows]
#print rowsA
  for rowA in rowsA:
    if(len(rowA) > 0):
      try:
        startTimesA   = [float(time_str) for time_str in strip_first(rowval(rowA,'Answer.startTimeList'),'|').split('|')]
        endTimesA     = [float(time_str) for time_str in strip_first(rowval(rowA,'Answer.endTimeList'),'|').split('|')]
        for rowB in rowsB:
          if(len(rowB) > 0):
            #print rowB
              try:
                startTimesB   = [float(time_str) for time_str in strip_first(rowval(rowB,'Answer.startTimeList'),'|').split('|')]
                endTimesB     = [float(time_str) for time_str in strip_first(rowval(rowB,'Answer.endTimeList'),'|').split('|')]
                #quals = mturk.get_qualification_score(action_annotation_type_id, rowval(rowA,'workerId'))
                #if any(workerId in s for s in qualified_workers): #show results from qualified workers only
                #if(len(quals) > 0 and quals[0].IntegerValue >= 50): #show results from qualified workers only
                #videoStartTime  = float(videoStartTimeStr)
                if(len(startTimesA) > 0 and len(startTimesB) > 0): #at least one annotation was made
                  #print startTimesArr
                  #startTimes = [videoStartTime + max(-1, float(t)) for t in startTimesArr]# if videoStartTime < target_end_time]
                  #endTimes = [videoStartTime + float(t) for t in endTimesArr]# if videoStartTime < target_end_time]
                  if(url2name(rowval(rowA,'Input.video_url_webm')) == target_video and url2name(rowval(rowB,'Input.video_url_webm')) == target_video):
                    if(float(rowval(rowA,'Input.start_time')) == float(target_start_time) and float(rowval(rowB,'Input.start_time')) == float(target_start_time)):
                      if(rowval(rowA,'WorkerId') != rowval(rowB,'WorkerId')): #don't compare worker against self in same video
                        curr_eam = calc_event_agreement(startTimesA,endTimesA,startTimesB,endTimesB)
                        #print rowval(rowA,'WorkerId') + " vs. " + rowval(rowB, 'WorkerId') + " = %.3f " % curr_eam
                        #data = []
                        dataA = []
                        dataB = []
                        for i in arange(0,10.1,0.1):
                          #print i
                          #print 'intervalsA: '
                          matchA = 0
                          matchB = 0
                          for startTimeA,endTimeA,startTimeB,endTimeB in zip(startTimesA,endTimesA,startTimesB,endTimesB):
                            if(i >= startTimeA and i <= endTimeA):
                              #print str(startTimeA) + "<->" + str(endTimeA)
                              matchA = 1
                            if(i >= startTimeB and i <= endTimeB):
                              matchB = 1
                          #print 'intervalsB: '
                          #for startTimeB,endTimeB in zip(startTimesB,endTimesB):
                          #    if(i >= startTimeB and i <= endTimeB):
                                  #print str(startTimeB) + "<->" + str(endTimeB)
                          #        matchB = 1
                          if(matchA):
                            dataA += ['1']
                          else:
                            dataA += ['0']
                          if(matchB):
                            dataB += ['1']
                          else:
                            dataB += ['0']
                        #print dataA
                        #data = ["    ".join(dataA), "    ".join(dataB)]
                        #print data
                        #array = [d.split() for d in data]  # convert to 2D list of string items
                        array = [dataA, dataB]  # convert to 2D list of string items
                        alp += [1-abs(krippendorff_alpha(array,nominal_metric,missing_items="*"))]
                        eam += [curr_eam]
                        sam += [calc_segmentation_agreement(startTimesA,endTimesA,startTimesB,endTimesB)]
                        #if(videoStartTime == target_start_time):
                          #    for t1,t2 in zip(startTimes,endTimes):
                          #        increment_dict(vid_time_diff, url2name(rowval(rowA,'Input.video_url_webm')), abs(t1-t2));
                          #        increment_dict(vid_time_count, url2name(rowval(rowA,'Input.video_url_webm')), 1);
              except ValueError:
                print 'Hit ' + rowval(rowB,'HITId') + ' contains no annotations!'
      except ValueError:
        print 'Hit ' + rowval(rowA,'HITId') + ' contains no annotations!'

data = (
    "0    1    1    1    1",
    "1    1    1    1    1",
    )

missing = '*' # indicator for missing values
array = [d.split() for d in data]  # convert to 2D list of string items

print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
print 'results for video ' + target_video + ' @ time %.0f:' %target_start_time
#print '\tnumber of matches: %d' % len(eam)
print "\tmean alpha : %.3f" % (sum(alp)/len(alp))
if(len(eam) > 0):
  print "\tmean eam   : %.3f" % (sum(eam)/len(eam))
else:
  print "\tmean eam   : undefined"
if(len(sam) > 0):
  print "\tmean sam   : %.3f" % (sum(sam)/len(sam))
else:
  print "\tmean sam   : undefined"
print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
