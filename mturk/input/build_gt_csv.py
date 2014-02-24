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

input_filenames = sys.argv
filenames = iter(input_filenames)
next(filenames) #skip first input argument (script name)
#if(len(input_filenames) > 3):
#    target_video = next(filenames)
for filename in filenames:
    csvreader = init_csv(filename,'r')
    rows = iter(csvreader)
    next(rows)
    gt_start_times_str = ''
    gt_end_times_str = ''
    gt_tags_str = ''
    for row in rows:
        gt_start_times_str += row[0]+'|'
        gt_end_times_str += row[1]+'|'
        gt_tags_str += row[2]+'|'
    gt_start_times = gt_start_times_str[0:-1]
    gt_end_times = gt_end_times_str[0:-1]
    gt_tags = gt_tags_str[0:-1]
    #print len(gt_end_times.split('|'))
    #print gt_start_times
    #print gt_end_times

videos = ['cmu_gt']#,'julia']
start_times = [0.0]
vid_resolutions = [8.07,32.28]
overlap_diviser = 1
max_resolution = vid_resolutions[-1]

csvwriter_all = init_csv('cmu_gt','w')

for resolution in vid_resolutions:
    csvwriter_eachres = init_csv('cmu_gt_'+str(int(resolution)),'w')
    for video,start_time in zip(videos,start_times):
        vidmp4 = url + video + '.mp4'
        vidwebm = url + video + '.webm'
        for i,j in zip( arange(start_time,start_time+max_resolution+resolution,resolution), \
                        arange(start_time+resolution/overlap_diviser,start_time+max_resolution+resolution,resolution)):
            if(i+resolution <= start_time+max_resolution):
                csvwriter_all.writerow([vidmp4, vidwebm, '', i, i+resolution,gt_start_times,gt_end_times,gt_tags])
                csvwriter_eachres.writerow([vidmp4, vidwebm, '', i, i+resolution,gt_start_times,gt_end_times,gt_tags])
            if(overlap_diviser != 1 and j+resolution <= start_time+max_resolution):
                csvwriter_all.writerow([vidmp4, vidwebm, '', j, j+resolution,gt_start_times,gt_end_times,gt_tags])
                csvwriter_eachres.writerow([vidmp4, vidwebm, '', j, j+resolution,gt_start_times,gt_end_times,gt_tags]) #empty title


#csvfile = open('input/from_output.csv', 'rb')
#csvreader = csv.reader(csvfile, delimiter=',')
#for row in csvreader:
#    print row
