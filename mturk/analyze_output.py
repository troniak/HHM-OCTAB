import csv
import sys
import re
from numpy import arange

headers = ['video_url_mp4', 'video_url_webm','title','start_time','end_time']
url = 'http://cs.ubc.ca/~troniak/'
template_name = 'analyze/analysis_template.html'
output_headers = ['HITId', 'HITTypeId', 'Title', 'Description', 'Keywords', 'Reward', 'CreationTime', 'MaxAssignments', 'RequesterAnnotation', 'AssignmentDurationInSeconds', 'AutoApprovalDelayInSeconds', 'Expiration', 'NumberOfSimilarHITs', 'LifetimeInSeconds', 'AssignmentId', 'WorkerId', 'AssignmentStatus', 'AcceptTime', 'SubmitTime', 'AutoApprovalTime', 'ApprovalTime', 'RejectionTime', 'RequesterFeedback', 'WorkTimeInSeconds', 'LifetimeApprovalRate', 'Last30DaysApprovalRate', 'Last7DaysApprovalRate', 'Input.video_url_mp4', 'Input.video_url_webm', 'Input.title', 'Input.start_time', 'Input.end_time', 'Answer.annotationText', 'Answer.endTimeList', 'Answer.noMoreActions', 'Answer.startTimeList', 'Approve', 'Reject']
inputs = sys.argv
output_name = inputs[1] #skip first input argument (script name)

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

csvreader = init_csv('output/'+output_name,'rb')
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

    reader = init_file(template_name,'rb')
    writer = init_file('analyze/analysis_'+hitId,'wb')

    start_pattern = '${start_times}'
    end_pattern   = '${end_times}'
    vidsrc_pattern = '${vid_src}'

    for line in reader:
        if(line.find(start_pattern) != -1):
            writer.write(line.replace(start_pattern,startTimes))
        elif(line.find(end_pattern) != -1):
            writer.write(line.replace(end_pattern,endTimes))
        elif(line.find(vidsrc_pattern) != -1):
            writer.write(line.replace(vidsrc_pattern,webmFilename))
        else:
            writer.write(line)
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
