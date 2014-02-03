import csv
import sys
import re
from numpy import arange
import os
from matplotlib import pyplot as plt

headers = ['video_url_mp4', 'video_url_webm','title','start_time','end_time']
url = 'http://cs.ubc.ca/~troniak/'
template_name = 'analyze/template.html'
output_headers = ['HITId', 'HITTypeId', 'Title', 'Description', 'Keywords', 'Reward', 'CreationTime', 'MaxAssignments', 'RequesterAnnotation', 'AssignmentDurationInSeconds', 'AutoApprovalDelayInSeconds', 'Expiration', 'NumberOfSimilarHITs', 'LifetimeInSeconds', 'AssignmentId', 'WorkerId', 'AssignmentStatus', 'AcceptTime', 'SubmitTime', 'AutoApprovalTime', 'ApprovalTime', 'RejectionTime', 'RequesterFeedback', 'WorkTimeInSeconds', 'LifetimeApprovalRate', 'Last30DaysApprovalRate', 'Last7DaysApprovalRate', 'Input.video_url_mp4', 'Input.video_url_webm', 'Input.title', 'Input.start_time', 'Input.end_time', 'Answer.annotationText', 'Answer.endTimeList', 'Answer.noMoreActions', 'Answer.startTimeList', 'Approve', 'Reject']
inputs = sys.argv
output_name= inputs[1] #skip first input argument (script name)
wordcounts = {} #counts frequency of words within all annotations
segcounts  = {} #counts # segments per video
vidcounts  = {} #counts # times video was annotated

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

def plot_dict(diction):
    min_frequency = 2
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

def url2name(url):
    return url[url.rfind('/')+1:url.rfind('.')]

csvreader = init_csv('output/'+output_name,'rb')
output_dir_name = 'analyze/'+output_name+'/'
mkdir(output_dir_name)
rows = iter(csvreader)
next(rows)
for row in rows:
    hitId           = row[output_headers.index('HITId')]
    mp4Filename     = row[output_headers.index('Input.video_url_mp4')]
    webmFilename    = row[output_headers.index('Input.video_url_webm')]
    videoStartTime  = row[output_headers.index('Input.start_time')]
    videoEndTime    = row[output_headers.index('Input.end_time')]
    noMoreActions   = row[output_headers.index('Answer.noMoreActions')]
    videoTitles     = strip_first(row[output_headers.index('Answer.annotationText')],'|')
    startTimes      = strip_first(row[output_headers.index('Answer.startTimeList')],'|')
    endTimes        = strip_first(row[output_headers.index('Answer.endTimeList')],'|')

    writer = init_file(output_dir_name+'analysis_'+hitId+'.html','wb')
    reader = init_file(template_name,'rb')

    video_start_pattern = '${start_time}'
    video_end_pattern   = '${end_time}'
    webm_pattern   = '${video_url_webm}'
    tags_pattern   = '${tags}'
    start_pattern  = '${start_times}'
    end_pattern    = '${end_times}'
    no_more_pattern= '${no_more_actions}'
    vidsrc_pattern = '${vid_src}'

    increment_wordcounts (videoTitles.split('|'));
    increment_dict(segcounts, url2name(webmFilename), len(startTimes.split('|')));
    increment_dict(vidcounts, url2name(webmFilename), 1);

    for line in reader:
        if(line.find(video_start_pattern) != -1):
            writer.write(line.replace(video_start_pattern,videoStartTime))
        elif(line.find(video_end_pattern) != -1):
            writer.write(line.replace(video_end_pattern,videoEndTime))
        elif(line.find(webm_pattern) != -1):
            writer.write(line.replace(webm_pattern,webmFilename).replace('troniak','dtroniak').replace('ubc','cmu').replace('ca','edu'))
        elif(line.find(tags_pattern) != -1):
            writer.write(line.replace(tags_pattern,videoTitles))
        elif(line.find(start_pattern) != -1):
            writer.write(line.replace(start_pattern,startTimes))
        elif(line.find(end_pattern) != -1):
            writer.write(line.replace(end_pattern,endTimes))
        elif(line.find(no_more_pattern) != -1):
            writer.write(line.replace(no_more_pattern,noMoreActions))
        elif(line.find(vidsrc_pattern) != -1):
            writer.write(line.replace(vidsrc_pattern,webmFilename))
        else:
            writer.write(line)

#print wordcounts
print vidcounts
plot_dict(wordcounts)
plot_dict(segcounts)
#plot_dict(vidcounts)

    #print videoTitles, startTimes, endTimes
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
