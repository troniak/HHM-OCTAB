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
from mturk import *

mturk = new_mturk_connection()
headers = ['video_url_mp4', 'video_url_webm','title','start_time','end_time']
url = 'http://cs.ubc.ca/~troniak/'
template_name = 'template.html'
qualified_workers = ['A248D5XVN1YGCZ', 'A2QAJ8BJ5QBB9A', 'A2WRSEO8HQRG5K', 'A37P0EXFVTAP0D', 'A38KIO2400LOTJ', 'A3DY78Q4FCWTXX', 'A3N87BX6PS0SIB', 'A9XWAWNLJN8DA']
action_annotation_type_id = '276M25L8I9N3M15OL9FEFQW7T8OIS7'
videos = [      'bike', '50salad',  'cmu_salad','pbj',  'tum']#,'julia']
start_times = [ 0.0,    180.0,      120.0,      2.0,    15.0]
videos = [      'bike','bike','bike', '50salad', '50salad','50salad', 'cmu_salad', 'cmu_salad', 'cmu_salad','pbj','pbj','pbj','tum','tum','tum']#,'julia']
start_times = [ 0.0,10.0,20.0,           180.0,190.0,200.0,               120.0,130.0,140.0,                   2.0,12.0,22.0,    15.0,25.0,35.0]
target_video = 'bike'
target_start_time = 0.0+10
inputs = sys.argv
time_diff_sum = 0
time_diff_count = 0
output_name= inputs[1] #skip first input argument (script name)
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

def init_file(name,mode):
    open(name, mode).close()
    f = open(name, mode)
    return f

def init_csv(name,mode):
    open(name+'.csv', mode).close()
    csvfile = open(name+'.csv', mode)
    if(mode == 'wb'):
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(headers)
        return csvwriter
    elif(mode == 'rb'):
        csvreader = csv.reader(csvfile, delimiter=',')
        return csvreader

#strip first in delim-separated string of elements
def strip_first(to_strip,delim):
    first_delim = to_strip.find(delim)
    if(first_delim != -1):
        to_strip = to_strip[first_delim+1:]
    else:
        to_strip = ''
    return to_strip

def mkdir(dir_name):
    try:
        os.mkdir(dir_name)
    except OSError:
        print 'dir ' + dir_name + ' already exists'

def increment_wordcounts(annotationArr):
    for annotation in annotationArr:
        words = annotation.split()
        for word in words:
            if(wordcounts.has_key(word)):
                wordcounts[word] = wordcounts[word] + 1
            else:
                wordcounts[word] = 1

def increment_dict(diction, key, num_increment):
    if(diction.has_key(key)):
        diction[key] = diction[key] + num_increment
    else:
        diction[key] = num_increment

"""
def append_to_dict(diction, key, value):
    if(diction.has_key(key)):
        diction[key] = diction[key].append(value)
    else:
        diction[key] = [value]
"""

def plot_dict(diction):
    min_frequency = 0.05 * max(diction.values())
    diction = dict((key, frequency) for key, frequency in diction.items() if frequency >= min_frequency)
    alphab = diction.keys()
    frequencies = diction.values()
    #d = dict((k, v) for k, v in d.items() if v >= 10)
    pos = arange(len(frequencies))
    width = 1.0     # gives histogram aspect to the bar diagram

    ax = plt.axes()
    ax.set_xticks(pos)# + (width / 2))
    ax.set_xticklabels(alphab, rotation=45, fontsize=8)
    ax.set_ylabel('frequencies')

    plt.bar(pos, frequencies, width, color='r')
    plt.show()

def dict_ratio(d1, d2):
    value_ratio = divide(array(d1.values()), array(d2.values()))
    d3 = {k:v for k,v in zip(d1.keys(),value_ratio)}
    return d3

def url2name(url):
    return url[url.rfind('/')+1:url.rfind('.')]

output_dir_name = ''+output_name+'/'
if(os.path.isfile('/Users/troniak/Downloads/'+output_name+'.csv')):
    shutil.move('/Users/troniak/Downloads/'+output_name+'.csv', '../output/'+output_name+'.csv')

for a in [1]:#target_video,target_start_time in zip(videos,start_times):
    csvreader = init_csv('../output/'+output_name,'rb')
#sortedlist = sorted(csvreader, key=operator.itemgetter(3), reverse=True)
    if(os.path.isfile(output_dir_name)):
        shutil.rmtree(output_dir_name)
    mkdir(output_dir_name)
    rows = iter(csvreader)
    output_headers = next(rows)
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

        #quals = mturk.get_qualification_score(action_annotation_type_id, workerId)
        #if any(workerId in s for s in qualified_workers): #show results from qualified workers only
        if(1):#len(quals) > 0 and quals[0].IntegerValue >= 50): #show results from qualified workers only
                video_start_pattern = '${start_time}'
                video_end_pattern   = '${end_time}'
                webm_pattern        = '${video_url_webm}'
                tags_pattern        = '${tags}'
                start_pattern       = '${start_times}'
                end_pattern         = '${end_times}'
                no_more_pattern     = '${no_more_actions}'
                vidsrc_pattern      = '${vid_src}'
                title_pattern       = '${video_title}'

                increment_wordcounts (videoTitlesStr.split('|'));
                increment_dict(segcounts, url2name(webmFilename), len(startTimesStr.split('|')));
                increment_dict(vidcounts, url2name(webmFilename), 1);
                startTimesArr = startTimesStr.split('|')
                endTimesArr = endTimesStr.split('|')
                videoStartTime  = float(videoStartTimeStr)
                if(startTimesArr[0] != ''): #at least one annotation was made
                    #print startTimesArr
                    startTimes = [videoStartTime + max(-1, float(t)) for t in startTimesArr]# if videoStartTime < target_end_time]
                    endTimes = [videoStartTime + float(t) for t in endTimesArr]# if videoStartTime < target_end_time]
                    if(url2name(webmFilename) == target_video):
                        if(videoStartTime == target_start_time):
                            y = float(videoStartTimeStr)+counter#] * len(startTimes)
                            counter = counter + delta_counter
                            delta_y_counter = delta_counter / len(startTimes)
                            for startTime,endTime in zip(startTimes,endTimes):
                                start_end = [[startTime,y],[endTime,y]]
                                #print counter + (startTime - target_start_time) / (target_start_time+10)
                                y = y+delta_y_counter#counter + ((startTime - target_start_time) / (target_start_time+10) )
                                plt.plot(*zip(*itertools.chain.from_iterable(itertools.combinations(start_end, 2))), color = 'brown', marker = '|')
                                #plt.scatter(startTimes,y,color='red')
                                #plt.scatter(endTimes,y,color='blue')
                    for t1,t2 in zip(startTimes,endTimes):
                        increment_dict(vid_time_diff, url2name(webmFilename), abs(t1-t2));
                        increment_dict(vid_time_count, url2name(webmFilename), 1);

                    if(status == 'Submitted'): #only analyze results that have not yet been approved
                        #print 'writing file '+output_dir_name+'analysis_'+hitId+'.html'
                        writer = init_file(output_dir_name+'analysis_'+workerId+'_'+hitId+'.html','wb')
                        reader = init_file(template_name,'rb')
                        for line in reader:
                            if(line.find(video_start_pattern) != -1):
                                writer.write(line.replace(video_start_pattern,videoStartTimeStr))
                            elif(line.find(video_end_pattern) != -1):
                                writer.write(line.replace(video_end_pattern,videoEndTime))
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
                                writer.write(line.replace(title_pattern,workerId+':'+hitId))
                            else:
                                writer.write(line)

#print wordcounts
    plt.show()
    #savefig('foo.png')
    print 'number of videos annotated (/30): ' + str(vidcounts)
    print 'number of qualified workers: ' + str(len(qualified_workers))
    plot_dict(wordcounts)
    plot_dict(segcounts)
    plot_dict(dict_ratio(segcounts, vidcounts))
    print 'average time per annotation: ' + str(dict_ratio(vid_time_diff,vid_time_count))
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
