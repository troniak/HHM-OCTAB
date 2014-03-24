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


mturk = new_mturk_connection()


inputs = sys.argv
payments_filename   = inputs[1] #skip first input argument (script name)
assignments_filename= inputs[2] #skip first input argument (script name)
vidcounts  = {} #counts # times video was annotated
HITIds= [] #counts # times video was annotated
bonus_count = 0


if(os.path.isfile('/Users/troniak/Downloads/'+assignments_filename+'.csv')):
    shutil.move('/Users/troniak/Downloads/'+assignments_filename+'.csv', '../output/'+assignments_filename+'.csv')
if(os.path.isfile('/Users/troniak/Downloads/'+payments_filename+'.csv')):
    shutil.move('/Users/troniak/Downloads/'+payments_filename+'.csv', '../output/'+payments_filename+'.csv')


assignmentsreader   = init_csv('../output/'+assignments_filename,'rb')
rows = iter(assignmentsreader)
output_headers = next(rows)
for row in rows:
    #print row[output_headers.index('HITId')]
    HITIds += [row[output_headers.index('HITId')]]
#print HITIds
#print len(HITIds)


paymentsreader      = init_csv('../output/'+payments_filename,'rb')
rows = iter(paymentsreader)
output_headers = next(rows)
for row in rows:
    transID         = row[output_headers.index('Transaction ID')]
    initDate        = row[output_headers.index('Date Initiated')]
    postDate        = row[output_headers.index('Date Posted')]
    transType       = row[output_headers.index('Transaction Type')]
    payMethod       = row[output_headers.index('Payment Method')]
    recipID         = row[output_headers.index('Recipient ID')]
    amount          = row[output_headers.index('Amount')]
    hitID           = row[output_headers.index('HIT ID')]
    assignID        = row[output_headers.index('Assignment ID')]
    #print assignID
    #print any(assignID in s for s in HITIds)
    #if(transType == 'BonusPayment'):
        #print 'hid: ' + hitID
        #print 'isi: ' + str(hitID in HITIds)
        #print 'rid: ' + recipID
        #print 'amt: ' + amount
        #print '~~~~~'
    if(recipID == 'A3SKQPPOKCZU88' and transType == 'BonusPayment'):# and hitID in HITIds):
        print "" + hitID + " | " + postDate + " | " + amount
        bonus_count += float(amount)
print 'bonus_count: %0.2f ' % bonus_count


"""
        #quals = mturk.get_qualification_score(action_annotation_type_id, workerId)
        #if any(workerId in s for s in qualified_workers): #show results from qualified workers only
        #if(1):#len(quals) > 0 and quals[0].IntegerValue >= 50): #show results from qualified workers only
        if(workerId == 'A3SKQPPOKCZU88'): #certain workers results
                submit_count += 1
        #if(hitId == '2DJVP9746OQ5IIE0TTX7B51QLTB1LW'): #certain workers results
                video_start_pattern = '${start_time}'
                video_end_pattern   = '${end_time}'
                webm_pattern        = '${video_url_webm}'
                tags_pattern        = '${tags}'
                start_pattern       = '${start_times}'
                end_pattern         = '${end_times}'
                no_more_pattern     = '${no_more_actions}'
                vidsrc_pattern      = '${vid_src}'
                title_pattern       = '${video_title}'

                print annotation_count
                print startTimesStr
                increment_wordcounts (videoTitlesStr.split('|'));
                annotation_count += len(startTimesStr.split('|')) - 5
                bonus = max(0,len(startTimesStr.split('|'))-5) / 5.0 * 0.5;
                bonus = floor(bonus*2)/2.0
                bonus_count += bonus
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

                    #if(status == 'Submitted'): #only analyze results that have not yet been approved
                    if(1):
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
