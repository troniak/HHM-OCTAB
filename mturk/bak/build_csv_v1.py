import csv
from numpy import arange

headers = ['video_url_mp4', 'video_url_webm','start_time','end_time']
url = 'http://cs.ubc.ca/~troniak/'
videos = ['bike','50salad','cmu','pbj','tum']#,'julia']
start_times = [0.0,180.0,17.0,2.0,15.0]
vid_resolutions = [2.0, 5.0, 10.0, 20.0, 30.0]
overlap_diviser = 1
max_resolution = vid_resolutions[-1]

def init_csv(name):
    open('input/'+name+'.csv', 'w').close()
    csvfile = open('input/'+name+'.csv', 'a')
    csvwriter = csv.writer(csvfile, delimiter=',')
    csvwriter.writerow(headers)
    return csvwriter;

csvwriter_all = init_csv('5at5');

for resolution in vid_resolutions:
    csvwriter_eachres = init_csv('5at5_'+str(int(resolution)));
    for video,start_time in zip(videos,start_times):
        vidmp4 = url + video + '.mp4'
        vidwebm = url + video + '.webm'
        for i,j in zip( arange(start_time,start_time+max_resolution+resolution,resolution), \
                        arange(start_time+resolution/overlap_diviser,start_time+max_resolution+resolution,resolution)):
            if(i+resolution <= start_time+max_resolution):
                csvwriter_all.writerow([vidmp4, vidwebm, i, i+resolution])
                csvwriter_eachres.writerow([vidmp4, vidwebm, i, i+resolution])
            if(overlap_diviser != 1 and j+resolution <= start_time+max_resolution):
                csvwriter_all.writerow([vidmp4, vidwebm, j, j+resolution])
                csvwriter_eachres.writerow([vidmp4, vidwebm, j, j+resolution])

#csvfile = open('input/5at5.csv', 'rb')
#csvreader = csv.reader(csvfile, delimiter=',')
#for row in csvreader:
#    print row
