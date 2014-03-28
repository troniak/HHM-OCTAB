import boto.mturk.connection as conn
from collections import OrderedDict
from operator import itemgetter
import fileinput
from pprint import pprint
from math import *
import csv
import sys
from numpy import arange
import numpy as np
from matplotlib import pyplot as plt
import re

headers = ['HITId', 'WorkerID','Input.title','Input.start_time','Input.end_time','Answer.endTimeList','Answer.noMoreActions','Answer.startTimeList']
HIT_headers = ['HITId', 'HITTypeId', 'Title', 'Description', 'Keywords', 'Reward', 'CreationTime', 'MaxAssignments', 'RequesterAnnotation', 'AssignmentDurationInSeconds', 'AutoApprovalDelayInSeconds', 'Expiration', 'NumberOfSimilarHITs', 'LifetimeInSeconds', 'AssignmentId', 'WorkerId', 'AssignmentStatus', 'AcceptTime', 'SubmitTime', 'AutoApprovalTime', 'ApprovalTime', 'RejectionTime', 'RequesterFeedback', 'WorkTimeInSeconds', 'LifetimeApprovalRate', 'Last30DaysApprovalRate', 'Last7DaysApprovalRate', 'Input.video_url_mp4', 'Input.video_url_webm', 'Input.title', 'Input.start_time', 'Input.end_time', 'Answer.annotationText', 'Answer.endTimeList', 'Answer.noMoreActions', 'Answer.startTimeList', 'Approve', 'Reject']
worker_milestones = {
    'A3DY78Q4FCWTXX': [1, 8, 11, 16, 24, 27, 29, 33, 35, 40, 46, 58],
    'A3LNPBZXHKKAA7': [1, 2, 4, 21, 25, 26, 27, 43, 44, 54],
    'A3SKQPPOKCZU88': [1, 2, 5, 7, 17, 25, 44, 45, 48, 51, 56, 58],
    'AMMTPFOPT7RCU' : [1, 2, 5, 6, 11, 14, 15, 17, 21, 23, 27, 54, 56],
    'A2QAJ8BJ5QBB9A': [1, 12, 52, 63]
}
worker_evolution = {
    'A3DY78Q4FCWTXX': ['OR', 'DD', 'TU, BM', 'FM', 'FR', 'NV', 'AU', 'AO', 'NO', 'AU', 'LA','EOF'],
    'A3LNPBZXHKKAA7': ['AU, DD, BM', 'FM', 'AO', 'VA', 'FP', 'NO', 'NO', 'RA, AO', 'IA','EOF'],
    'A3SKQPPOKCZU88': ['TU', 'AO', 'AW', 'AP', 'AO', 'AU', 'AA', 'NO', 'IA', 'CA', 'UA','EOF'],
    'AMMTPFOPT7RCU' : ['SA', 'OR', 'DD', 'AA', 'FR', 'AO, AU, UC', 'FM', 'CA', 'NO', 'FR', 'FM', 'AO','EOF'],
    'A2QAJ8BJ5QBB9A': ['DD, OR, BM, FM', 'IA', 'AT','EOF']
}

#strip first in delim-separated string of elements
def strip_first(to_strip,delim):
    first_delim = to_strip.find(delim)
    if(first_delim != -1):
        to_strip = to_strip[first_delim+1:]
    else:
        to_strip = ''
    return to_strip

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

def increment_dict(diction, key, num_increment):
    if(diction.has_key(key)):
        diction[key] = diction[key] + num_increment
    else:
        diction[key] = num_increment

def plot_dict(diction):
    #min_frequency = 0.05 * max(diction.values())
    diction = dict((key, frequency) for key, frequency in diction.items())# if frequency >= min_frequency)
    alphab = diction.keys()
    frequencies = diction.values()
    #d = dict((k, v) for k, v in d.items() if v >= 10)
    pos = arange(len(frequencies))
    width = 1.0     # gives histogram aspect to the bar diagram

    ax = plt.axes()
    ax.set_xticks(pos)# + (width / 2))
    ax.set_xticklabels(alphab, rotation=45, fontsize=20)
    ax.set_ylabel('frequencies')

    plt.bar(pos, frequencies, width, color='r')
    plt.show()

mturk = conn.MTurkConnection(aws_access_key_id='AKIAJUL53VTH3ENYMNIQ', aws_secret_access_key='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', is_secure=True, port=None, proxy=None, proxy_port=None, proxy_user=None, proxy_pass=None, host=None, debug=0, https_connection_factory=None, security_token=None, profile_name=None)
bonuses = {}
submit_counts = {}
annotation_counts = {}
word_counts = {}
word_means_milestone = {}
word_stds_milestone = {}
annotation_counts_milestone = {}
milestone_counts = {}
#hits = get_all_hits(mturk)
hits = mturk.get_all_hits()
#print 'Number of HITs returned: %d' % len(list(hits)) #breaks hits construct
print 'Fetching assignments...'
csvwriter_all = init_csv(''+'results','w')
#output_headers = []
answers = {}
hitcount = 0
innerhitcount = 0
for hit in hits:
    if(1):
        hitcount += 1
        #output_headers += [hit.HITId]
        #output_headers += [hit.WorkerID]
        headers = ['HITId', 'WorkerID','Input.title','Input.start_time','Input.end_time','Answer.endTimeList','Answer.noMoreActions','Answer.startTimeList']
        assignments = mturk.get_assignments(hit.HITId)
        for assignment in assignments:
            #if(1):
            #if(assignment.AssignmentStatus == 'Submitted'):
            #if(assignment.WorkerId == 'A2QAJ8BJ5QBB9A'):
            if(assignment.WorkerId in worker_milestones.keys()):
                innerhitcount += 1
                #print "HIT# %d" % hitcount
                #print "Inner-loop HIT#: %d" % innerhitcount
                #print "Answers of the worker %s" % assignment.WorkerId
                a = 0
                for question_form_answer in assignment.answers[0]:
                    answers[hitcount] = question_form_answer
                    for value in question_form_answer.fields:
                      a += 1
                      #print 'field' + str(a) + ': ' + value
                #print 'work time (s): ' + assignment.WorkTimeInSeconds
                annotations_struct  = assignment.answers[0][2]
                annotations_str = annotations_struct.fields[0]
                annotations = strip_first(annotations_str,'|').split('|')
                numannotations = len(annotations)
                numwords = len(annotations_str.replace('|',' ').split(' '))
                #print 'annotations_str: ' + annotations_str
                #print 'numwords: %d' % numwords
                #print 'numannotations: %d' % numannotations
                bonus = max(0,numannotations-5) / 5.0 * 0.5;
                bonus = floor(bonus*2)/2.0
                #print 'bonus: ' + str(bonus)
                increment_dict(bonuses, assignment.WorkerId, bonus)
                increment_dict(submit_counts, assignment.WorkerId, 1)
                increment_dict(annotation_counts, assignment.WorkerId, numannotations)
                increment_dict(word_counts, assignment.WorkerId, numwords)

                #print words_per_annot

                if(submit_counts.get(assignment.WorkerId) in worker_milestones.get(assignment.WorkerId)):
                  words_per_annot = [len(re.findall(r'\w+', annot)) for annot in annotations]
                  increment_dict(milestone_counts,assignment.WorkerId,1)
                  print 'milestone ' + str(milestone_counts.get(assignment.WorkerId)) + ' for ' + assignment.WorkerId + ':'
                  word_mean = np.mean(words_per_annot)
                  word_std = np.std(words_per_annot)
                  #try:
                  #  word_mean = numwords / numannotations
                  #except ZeroDivisionError:
                  #  word_mean = 0
                  #print annotations_str
                  print 'number of submissions: %d' % submit_counts.get(assignment.WorkerId)
                  print 'number of annotations: %d' % numannotations
                  print 'mean wordcount per annotation: %f' % word_mean
                  print 'std wordcount per annotation: %f' % word_std
                  increment_dict(annotation_counts_milestone, assignment.WorkerId, [numannotations])
                  increment_dict(word_means_milestone, assignment.WorkerId, [word_mean])
                  increment_dict(word_stds_milestone, assignment.WorkerId, [word_std])
                  print "--------------------"
                #print hit
                #csvwriter.writerow([vidmp4, vidwebm, '', i, i+resolution])
print bonuses
print submit_counts
print annotation_counts
for key,value in annotation_counts_milestone.iteritems():
  wid = key
  annotation_counts = annotation_counts_milestone.get(wid)
  word_means = word_means_milestone.get(wid)
  word_stds = word_stds_milestone.get(wid)
  new_keys = worker_milestones.get(wid)
  #print new_keys
  new_keys = list(OrderedDict.fromkeys(new_keys)) #remove duplicates
  xticks = arange(0.5,len(annotation_counts),1)
  plt.bar(xticks, annotation_counts, alpha=0.5, label='#annotations/submission')
  plt.bar(xticks, word_means,color='red', alpha=0.5, label='#words/annotation',yerr=word_stds)
  plt.title('annotation evolution of worker ' + wid)
  plt.xlabel('milestones of sophistication')
  plt.ylabel('counts (annotations/submission, blue) and (words/annotation, red)')
  plt.xticks(xticks,zip(worker_evolution.get(wid),worker_milestones.get(wid)), rotation=30, fontsize=8)
  plt.legend(('#annotations/submission','#words/annotation'))
  plt.show()
  #print set(new_keys)
  #print sorted(set(new_keys))
  #print annotation_counts
  #sorted_zip = sorted(zip(new_keys,annotation_counts),key=itemgetter(0))
  #sorted_counts = [t[1] for t in sorted_zip]
  #print sorted_counts
  #print sorted_counts
  #new_dict = OrderedDict(zip(new_keys,annotation_counts))
  #print 'annotation count evolution for worker ' + wid
  #print new_dict
  #plot_dict(new_dict)
  #plt.bar(arange(0.5,len(sorted_counts),1), sorted_counts)
  """
for key,value in word_means_milestone.iteritems():
  wid = key
  new_values = value
  new_keys = worker_milestones.get(wid)
  new_keys = list(OrderedDict.fromkeys(new_keys)) #remove duplicates
  #print new_keys
  #print new_values
  xticks = arange(0.5,len(new_values),1)
  plt.bar(xticks, new_values)
  plt.title('word count evolution for worker ' + wid)
  plt.xlabel('milestones of annotation sophistication')
  plt.ylabel('mean # words per annotation in submission')
  plt.xticks(xticks,worker_evolution.get(wid), rotation=30, fontsize=10)
  plt.show()
  #sorted_zip = sorted(zip(new_keys,set(new_values)),key=itemgetter(0))
  #sorted_counts = [t[1] for t in sorted_zip]
  #print sorted_counts
  #new_dict = OrderedDict(zip(new_keys,new_values))
  #print 'annotation count evolution for worker ' + wid
  #print new_dict
  #plot_dict(new_dict)
  """

#print word_counts
#print word_means_milestone
#s = ''
#while(s != 'q'):
#    s = raw_input('Provide Hit# to view (q to quit): ')
#    print s
print 'Done!'
