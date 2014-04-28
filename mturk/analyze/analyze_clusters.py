import csv
import sys
from io_utils import *
from utils import *
from operator import itemgetter

url = 'http://cs.ubc.ca/~troniak/'
output_name= sys.argv[1] #skip first input argument (script name)
output_dir_name = ''+output_name+'/'
template_name = 'template.html'
if(os.path.isdir(output_dir_name)):
    shutil.rmtree(output_dir_name)
mkdir(output_dir_name)
writer = init_file(output_dir_name+'analysis_cluster.html','wb')
reader = init_file(template_name,'rb')

mp4Filename     = url+'50salad.mp4'
webmFilename    = url+'50salad.webm'
videoStartTime  =180
videoEndTime    =210
videoStartTimeStr=str(videoStartTime)
videoEndTimeStr  =str(videoEndTime)
#noMoreActions   = row[output_headers.index('Answer.noMoreActions')]
startTimes   = [195.960000000000,201.460000000000,204.080000000000,200.080000000000,199.600000000000,200.440000000000,186.080000000000,200.840000000000,190.960000000000,205.080000000000,197.080000000000,185.280000000000,197.760000000000,208.120000000000,186.720000000000,204.800000000000,184.760000000000,207.200000000000,183.160000000000,181.080000000000,197.380000000000,180.080000000000,194.920000000000,206.720000000000,199.280000000000,182.440000000000,196.920000000000,187.640000000000,185.140000000000,183.900000000000,198,193.880000000000,181.760000000000,198.520000000000,188.520000000000,203.200000000000,209.080000000000,203.480000000000,190.080000000000,180.520000000000,183.120000000000,205.080000000000,195.240000000000,192.720000000000,189.320000000000,194.360000000000,205.600000000000,202.080000000000,193.240000000000,206.280000000000]
endTimes     = [197,202.060000000000,205.040000000000,200.520000000000,200.040000000000,200.920000000000,186.720000000000,201.320000000000,191.840000000000,206.640000000000,197.920000000000,185.960000000000,198.520000000000,209,187.240000000000,205.520000000000,185.200000000000,208.120000000000,183.800000000000,182.560000000000,197.740000000000,180.400000000000,196.720000000000,207.180000000000,199.600000000000,183.120000000000,197.720000000000,188.520000000000,188.600000000000,184.720000000000,200.080000000000,195.140000000000,182.280000000000,199.240000000000,190.040000000000,203.440000000000,209.520000000000,204,190.840000000000,181.040000000000,184.720000000000,205.640000000000,195.760000000000,193,190,194.720000000000,206.480000000000,203,193.720000000000,206.680000000000]
videoTitles   = ['cluster'+str(i) for i in arange(len(startTimes))]

#print [startTime - videoStartTime for startTime in startTimes]
#print [endTime - videoStartTime for endTime in endTimes]

sorted_times    = sorted(zip(startTimes,endTimes),key=itemgetter(0))
startTimesStrArr= [str(times[0]-videoStartTime) for times in sorted_times]
endTimesStrArr  = [str(times[1]-videoStartTime) for times in sorted_times]
startTimesStr   = '|'.join(startTimesStrArr)
endTimesStr     = '|'.join(endTimesStrArr)
videoTitlesStr  = '|'.join(videoTitles)

#print startTimesStr
#print endTimesStr
#"""
video_start_pattern = '${start_time}'
video_end_pattern   = '${end_time}'
webm_pattern        = '${video_url_webm}'
tags_pattern        = '${tags}'
start_pattern       = '${start_times}'
end_pattern         = '${end_times}'
no_more_pattern     = '${no_more_actions}'
vidsrc_pattern      = '${vid_src}'
title_pattern       = '${video_title}'

for line in reader:
  if(line.find(video_start_pattern) != -1):
      writer.write(line.replace(video_start_pattern,videoStartTimeStr))
  elif(line.find(video_end_pattern) != -1):
      writer.write(line.replace(video_end_pattern,videoEndTimeStr))
  elif(line.find(webm_pattern) != -1):
      writer.write(line.replace(webm_pattern,webmFilename).replace('troniak','dtroniak').replace('ubc','cmu').replace('ca','edu'))
  elif(line.find(tags_pattern) != -1):
      writer.write(line.replace(tags_pattern,videoTitlesStr))
  elif(line.find(start_pattern) != -1):
      writer.write(line.replace(start_pattern,startTimesStr))
  elif(line.find(end_pattern) != -1):
      writer.write(line.replace(end_pattern,endTimesStr))
  #elif(line.find(no_more_pattern) != -1):
      #writer.write(line.replace(no_more_pattern,noMoreActions))
  elif(line.find(vidsrc_pattern) != -1):
      writer.write(line.replace(vidsrc_pattern,webmFilename))
  elif(line.find(title_pattern) != -1):
      writer.write(line.replace(title_pattern,''))
  else:
      writer.write(line)
      #"""
