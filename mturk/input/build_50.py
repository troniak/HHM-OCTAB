import csv
import sys
from numpy import arange

headers = ['video_url_mp4', 'video_url_webm','title','start_time','end_time','gt_start_times','gt_end_times','gt_tags']
url = 'http://cs.ubc.ca/~troniak/'
input_filenames = sys.argv
target_video = ''
min_annotation_size = 0.5

def url2name(url):
    return url[url.rfind('/')+1:url.rfind('.')]

def init_csv(name,mode):
    open(name+'.csv', mode).close()
    csvfile = open(name+'.csv', mode)
    if(mode == 'w'):
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(headers)
        return csvwriter
    elif(mode == 'r'):
        csvreader = csv.reader(csvfile, delimiter=',')
        return csvreader

if(len(input_filenames) > 1):
    #output_headers = ['HITId', 'HITTypeId', 'Title', 'Description', 'Keywords', 'Reward', 'CreationTime', 'MaxAssignments', 'RequesterAnnotation', 'AssignmentDurationInSeconds', 'AutoApprovalDelayInSeconds', 'Expiration', 'NumberOfSimilarHITs', 'LifetimeInSeconds', 'AssignmentId', 'WorkerId', 'AssignmentStatus', 'AcceptTime', 'SubmitTime', 'AutoApprovalTime', 'ApprovalTime', 'RejectionTime', 'RequesterFeedback', 'WorkTimeInSeconds', 'LifetimeApprovalRate', 'Last30DaysApprovalRate', 'Last7DaysApprovalRate', 'Input.video_url_mp4', 'Input.video_url_webm', 'Input.title', 'Input.start_time', 'Input.end_time', 'Answer.annotationText', 'Answer.endTimeList', 'Answer.noMoreActions', 'Answer.startTimeList']
    filenames = iter(input_filenames)
    next(filenames) #skip first input argument (script name)
    if(len(input_filenames) > 3):
        target_video = next(filenames)
    output_name = next(filenames)
    csvwriter_all = init_csv(''+output_name,'w')
    for filename in filenames:
        csvreader = init_csv(filename,'r')
        rows = iter(csvreader)
        output_headers = next(rows)
        for row in rows:
            #print row
            mp4Filename = row[output_headers.index('Input.video_url_mp4')]
            webmFilename = row[output_headers.index('Input.video_url_webm')]
            if(target_video != '' and url2name(webmFilename) == target_video):
                baseTime = row[output_headers.index('Input.start_time')]
                #skip header element
                videoTitles = iter(row[output_headers.index('Answer.annotationText')].split('|'))
                startTimes = iter(row[output_headers.index('Answer.startTimeList')].split('|'))
                endTimes = iter(row[output_headers.index('Answer.endTimeList')].split('|'))
                next(videoTitles);
                next(startTimes);
                next(endTimes);
                for videoTitle,startTime,endTime in zip(videoTitles,startTimes,endTimes):
                    if(abs(float(startTime)-float(endTime)) > min_annotation_size):
                        absStartTime = float(baseTime)+float(startTime)
                        absEndTime = float(baseTime)+float(endTime)
                        csvwriter_all.writerow([mp4Filename,webmFilename,videoTitle,str(absStartTime),str(absEndTime)])
else:
    videos = ['50salad']#,'cmu_salad']#,'julia']
    start_times = [20.0]
    vid_resolutions = [10.0]
    overlap_diviser = 1
    max_resolution = 350.0#vid_resolutions[-1]

    csvwriter_all = init_csv(''+'5at5','w')

    for resolution in vid_resolutions:
        csvwriter_eachres = init_csv(''+'5at5_'+str(int(resolution)),'w')
        for video,start_time in zip(videos,start_times):
            vidmp4 = url + video + '.mp4'
            vidwebm = url + video + '.webm'
            for i,j in zip( arange(start_time,start_time+max_resolution+resolution,resolution), \
                            arange(start_time+resolution/overlap_diviser,start_time+max_resolution+resolution,resolution)):
                if(i+resolution <= start_time+max_resolution):
                    csvwriter_all.writerow([vidmp4, vidwebm, '', i, i+resolution])
                    csvwriter_eachres.writerow([vidmp4, vidwebm, '', i, i+resolution])
                if(overlap_diviser != 1 and j+resolution <= start_time+max_resolution):
                    csvwriter_all.writerow([vidmp4, vidwebm, '', j, j+resolution])
                    csvwriter_eachres.writerow([vidmp4, vidwebm, '', j, j+resolution]) #empty title


#csvfile = open('from_output.csv', 'rb')
#csvreader = csv.reader(csvfile, delimiter=',')
#for row in csvreader:
#    print row
