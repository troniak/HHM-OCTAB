import csv
import sys
import re
from numpy import arange
from numpy import divide
from numpy import array
import numpy as np
import os
import shutil
from io_utils import *
from utils import *
from matplotlib import pyplot as plt
import itertools
from mturk import *
from pylab import *
import random

mturk = new_mturk_connection()

url = 'http://cs.ubc.ca/~troniak/'
template_name = 'template_rand2.html'
videos = [      'bike', '50salad',  'cmu_salad','pbj',  'tum']#,'julia']
start_times = [ 0.0,    180.0,      120.0,      2.0,    15.0]
videos = [      'bike','bike','bike', '50salad', '50salad','50salad', 'cmu_salad', 'cmu_salad', 'cmu_salad','pbj','pbj','pbj','tum','tum','tum']#,'julia']
start_times = [ 0.0,10.0,20.0,           180.0,190.0,200.0,               120.0,130.0,140.0,                   2.0,12.0,22.0,    15.0,25.0,35.0]
target_video = '50salad'
target_start_time = 180.0+10
inputs = sys.argv
output_name= inputs[1] #skip first input argument (script name)

output_dir_name = ''+output_name+'/'
if(os.path.isfile('/Users/troniak/Downloads/'+output_name+'.csv')):
    shutil.move('/Users/troniak/Downloads/'+output_name+'.csv', '../output/'+output_name+'.csv')

annotation_selections = [("She positions the tomato slice back next to the tomato half", "She grasps some of the lettuce inside the bag with her right hand."), ("She allows the tomato halfs to fall to each side of the knife", "She rotates the tomato slightly clockwise on the cutting board with both hands"), ("With her right hand, she stirs the vegetables in the bowl", "Taking the piece of cabbage in the spoon to the mouth for eating"), ("She leans into the counter", "He walks to the table in the center of the room"), ("Again arranging the tomato pieces in the table", "Preparing to cut the cabbage into further pieces")]


for a in [1]:#target_video,target_start_time in zip(videos,start_times):
#for target_video,target_start_time in zip(videos,start_times):
    csvreader = init_csv('../output/'+output_name,'rb')
    if(os.path.isdir(output_dir_name)):
        shutil.rmtree(output_dir_name)
    mkdir(output_dir_name)
    rows = iter(csvreader)
    output_headers = next(rows)
    print output_headers
    videoTitles = []
    startTimes = []
    endTimes = []
    for row in rows:
        webmFilename    = row[output_headers.index('Input.video_url_webm')]
        video_start_time= row[output_headers.index('Input.start_time')]
        video_end_time= row[output_headers.index('Input.end_time')]
        #if(url2name(webmFilename) == target_video):
        if(1):
          videoTitlesStr  = strip_first(row[output_headers.index('Answer.annotationText')],'|')
          startTimesStr   = strip_first(row[output_headers.index('Answer.startTimeList')],'|')
          endTimesStr     = strip_first(row[output_headers.index('Answer.endTimeList')],'|')
          videoTitles += [videoTitleStr for videoTitleStr in videoTitlesStr.split('|')]
          startTimes  += [str(float(startTimeStr)+float(video_start_time))  for startTimeStr in startTimesStr.split('|')]
          endTimes    += [str(float(endTimeStr)+float(video_start_time)) for endTimeStr in endTimesStr.split('|')]

video_start_pattern = '${start_time}'
video_end_pattern   = '${end_time}'
webm_pattern        = '${video_url_webm}'
tags_pattern        = '${tags}'
start_pattern       = '${start_times}'
end_pattern         = '${end_times}'
no_more_pattern     = '${no_more_actions}'
vidsrc_pattern      = '${vid_src}'
title_pattern       = '${video_title}'

video_start_pattern2 = '${start_time2}'
video_end_pattern2   = '${end_time2}'
webm_pattern2        = '${video_url_webm2}'
tags_pattern2        = '${tags2}'
start_pattern2       = '${start_times2}'
end_pattern2         = '${end_times2}'
no_more_pattern2     = '${no_more_actions2}'
vidsrc_pattern2      = '${vid_src2}'
title_pattern2       = '${video_title2}'
webmFilename        = url + target_video + '.webm'
#print zip(startTimes,endTimes,videoTitles)
#zipped1 = zip(startTimes,endTimes,videoTitles)
#zipped2 = zip(startTimes,endTimes,videoTitles)
#random.shuffle(zipped1)
#random.shuffle(zipped2)
#allzip = zip(zipped1,zipped2)
#allzip = [e1 + e2 for e1,e2 in zip(zipped1,zipped2)]
#print tuple(list(allzip[0]) + [allzip[1]])
#print zipped2
#print zip(e1(1),e1(2),e1(3),e2(1),e2(2),e2(3) for zipped1,zipped2)
#print zip(random.shuffle(zip(startTimes,endTimes,videoTitles)),random.shuffle(zip(startTimes,endTimes,videoTitles)))
for startTime,endTime,title in zip(startTimes,endTimes,videoTitles):
  for startTime2,endTime2,title2 in zip(startTimes,endTimes,videoTitles):
    for annotation_selection in annotation_selections:
      #print 'title: '+title
      #print 'select: '+annotation_selection[1]
      if(title == annotation_selection[1]):# or title2 == annotation_selection[1]):
          #print 'writing file '+output_dir_name+'analysis_'+hitId+'.html'
          output_filename = 'analysis_'+title+'-vs-'+title2+'.html'
          writer = init_file(output_dir_name+output_filename.replace('/',' or ').replace(' ','_'),'wb')
          reader = init_file(template_name,'rb')
          for line in reader:
              if(line.find(video_start_pattern) != -1):
                  writer.write(line.replace(video_start_pattern,startTime))
              elif(line.find(video_end_pattern) != -1):
                  writer.write(line.replace(video_end_pattern,endTime))
              elif(line.find(webm_pattern) != -1):
                  writer.write(line.replace(webm_pattern,webmFilename).replace('troniak','dtroniak').replace('ubc','cmu').replace('ca','edu'))
              elif(line.find(tags_pattern) != -1):
                  writer.write(line.replace(tags_pattern,''))
              elif(line.find(start_pattern) != -1):
                  writer.write(line.replace(start_pattern,''))
              elif(line.find(end_pattern) != -1):
                  writer.write(line.replace(end_pattern,''))
              #elif(line.find(no_more_pattern) != -1):
                  #writer.write(line.replace(no_more_pattern,noMoreActions))
              elif(line.find(vidsrc_pattern) != -1):
                  writer.write(line.replace(vidsrc_pattern,webmFilename))
              elif(line.find(title_pattern) != -1):
                  writer.write(line.replace(title_pattern,title))
              elif(line.find(video_start_pattern2) != -1):
                  writer.write(line.replace(video_start_pattern2,startTime2))
              elif(line.find(video_end_pattern2) != -1):
                  writer.write(line.replace(video_end_pattern2,endTime2))
              elif(line.find(webm_pattern2) != -1):
                  writer.write(line.replace(webm_pattern2,webmFilename).replace('troniak','dtroniak').replace('ubc','cmu').replace('ca','edu'))
              elif(line.find(tags_pattern2) != -1):
                  writer.write(line.replace(tags_pattern2,''))
              elif(line.find(start_pattern2) != -1):
                  writer.write(line.replace(start_pattern2,''))
              elif(line.find(end_pattern2) != -1):
                  writer.write(line.replace(end_pattern2,''))
              #elif(line.find(no_more_pattern2) != -1):
                  #writer.write(line.replace(no_more_pattern2,noMoreActions))
              elif(line.find(vidsrc_pattern2) != -1):
                  writer.write(line.replace(vidsrc_pattern2,webmFilename))
              elif(line.find(title_pattern2) != -1):
                  writer.write(line.replace(title_pattern2,title2))
              else:
                  writer.write(line)

"""

      for row in rows:
          hitId           = row[output_headers.index('HITId')]
          workerId        = row[output_headers.index('WorkerId')]
          status          = row[output_headers.index('AssignmentStatus')]
          mp4Filename     = row[output_headers.index('Input.video_url_mp4')]
          webmFilename    = row[output_headers.index('Input.video_url_webm')]
          videoStartTimeStr  = row[output_headers.index('Input.start_time')]
          videoEndTime    = row[output_headers.index('Input.end_time')]
          #noMoreActions   = row[output_headers.index('Answer.noMoreActions')]
          videoTitlesStr  = strip_first(row[output_headers.index('Answer.annotationText')],'|')
          startTimesStr   = strip_first(row[output_headers.index('Answer.startTimeList')],'|')
          endTimesStr     = strip_first(row[output_headers.index('Answer.endTimeList')],'|')
          videoTitles     = [videoTitlesStr in videoTitlesStr.split('|')]
          startTimes      += [startTimeStr   in startTimesStr.split('|')]
          endTimes        += [endTimeStr     in endTimesStr.split('|')]

          #quals = mturk.get_qualification_score(action_annotation_type_id, workerId)
          #if any(workerId in s for s in qualified_workers): #show results from qualified workers only
          if(1):#len(quals) > 0 and quals[0].IntegerValue >= 50): #show results from qualified workers only
          #if(workerId == 'A3SKQPPOKCZU88'): #certain workers results
          #if(hitId == '2DJVP9746OQ5IIE0TTX7B51QLTB1LW'): #certain workers results
                  submit_count += 1
                  video_start_pattern = '${start_time}'
                  video_end_pattern   = '${end_time}'
                  webm_pattern        = '${video_url_webm}'
                  tags_pattern        = '${tags}'
                  start_pattern       = '${start_times}'
                  end_pattern         = '${end_times}'
                  no_more_pattern     = '${no_more_actions}'
                  vidsrc_pattern      = '${vid_src}'
                  title_pattern       = '${video_title}'

#print wordcounts
    #plt.show()
    plt.savefig('../output/figures/' + '_' + str(loopcount) + '_' + str(target_video) + '_' + str(target_start_time) + '.png')    #save("signal", ext="png", close=False, verbose=True)
    plt.close()
    print 'submit_count: ' + str(submit_count)
    print 'annotation_count: ' + str(annotation_count)
    print 'bonus_count: ' + str(bonus_count)
    #print 'number of videos annotated (/30): ' + str(vidcounts)
    #plot_dict(wordcounts)
    #plot_dict(segcounts)
    #plot_dict(dict_ratio(segcounts, vidcounts))
    #print 'average time per annotation: ' + str(dict_ratio(vid_time_diff,vid_time_count))
#print vid_time_diff
#print vid_time_count
#plot_dict(vidcounts)

        #print videoTitlesStr, startTimesStr, endTimesStr
        #skip header element
        #videoTitles = iter(row[output_headers.index('Answer.annotationText')].split('|'))
        #startTimes = iter(row[output_headers.index('Answer.startTimeList')].split('|'))
        #endTimes = iter(row[output_headers.index('Answer.endTimeList')].split('|'))
        #next(videoTitles);
        #next(startTimes);
        #next(endTimes);
        #for videoTitle in zip(videoTitles,startTimes,endTimes):
        #    absStartTime = float(baseTime)+float(startTime)
        #    absEndTime = float(baseTime)+float(endTime)
        #    csvwriter_all.writerow([mp4Filename,webmFilename,videoTitle,str(absStartTime),str(absEndTime)])
"""
