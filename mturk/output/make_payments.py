import boto.mturk.connection as conn
from boto.mturk.price import Price
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
from mturk import *
import datetime
import time

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

#e.g. mturk time string: 2014-04-19T19:36:32Z
def parse_mturk_time(time_str,return_time_part=''):
  ymd = time_str.split('-')
  dt  = ymd[2].split('T')
  hms = dt[1].replace('Z','').split(':')
  #print 'ymd:'+str(ymd)
  #print 'dt:'+str(dt)
  #print 'hms:'+str(hms)
  if(return_time_part=='y'):
    return ymd[0]
  elif(return_time_part=='mo'):
    return ymd[1]
  elif(return_time_part=='d'):
    return dt[0]
  elif(return_time_part=='t'):
    return dt[1]
  elif(return_time_part=='h'):
    return hms[0]
  elif(return_time_part=='mi'):
    return hms[1]
  elif(return_time_part=='s'):
    return hms[2]
  else:
    return ''

def mtime2datetime(mturk_time_str):
  return datetime.datetime(int(parse_mturk_time(mturk_time_str,'y')), int(parse_mturk_time(mturk_time_str,'mo')), int(parse_mturk_time(mturk_time_str,'d')), int(parse_mturk_time(mturk_time_str,'h')), int(parse_mturk_time(mturk_time_str,'mi')))

def pay_bonuses(bonuses,i):
  worker_id = bonuses.keys()[i]
  print 'worker %s: approve all assignments and pay %f bonus?' % (bonuses.keys()[i],bonus_totals[i])
  answer = raw_input('yes/no: ')
  if(answer == 'yes'):
    for bonus in bonuses.values()[i]:
      assignment_id = bonus[0]
      amount = bonus[1]
      if(amount > 0):
        annotation_count = bonus[2]
        reason = 'Extra ' + str(annotation_count) + ' annotations. Thank you very much!'
        pay_bonus(mturk, worker_id, assignment_id, amount, reason)
        #print reason
      mturk.approve_assignment(assignment_id)
    print 'bonus paid!'
  else:
    print 'bonus not paid'

mturk = new_mturk_connection()
#mturk.assign_qualification('3FQWXCP5BAA4IJ9RR8PWI2Z94YQ4HQ', 'A2V3P1XE33NYC3')
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
#hits = get_all_reviewable_hits(mturk)
#print 'Number of HITs returned: %d' % len(list(hits)) #breaks hits construct
print 'Fetching assignments...'
csvwriter_all = init_csv(''+'results','w')
#output_headers = []
answers = {}
hitcount = 0
innerhitcount = 0
mturk_test_time = '2014-04-01T00:00:00Z'
#print dir(hits[0])
#print hits[0].expired
for hit in hits:
    if(1):
        hitcount += 1
        #output_headers += [hit.HITId]
        #output_headers += [hit.WorkerID]
        headers = ['HITId', 'WorkerID','Input.title','Input.start_time','Input.end_time','Answer.endTimeList','Answer.noMoreActions','Answer.startTimeList']
        assignments = mturk.get_assignments(hit.HITId)
        #reward = hit.Reward
        #print reward
        for assignment in assignments:
            #if(1):
            if(assignment.AssignmentStatus == 'Submitted'):
            #if(assignment.WorkerId == 'A3SKQPPOKCZU88'):
            #if(assignment.WorkerId in worker_milestones.keys()):
                innerhitcount += 1
                print "HIT# %d" % hitcount
                print "Inner-loop HIT#: %d" % innerhitcount
                print "Answers of the worker %s" % assignment.WorkerId
                approval_time = ''
                rejection_time = ''
                try:
                  approval_time = str(assignment.ApprovalTime)
                  print "Approval Time: " + approval_time
                except AttributeError:
                  try:
                    rejection_time = str(assignment.RejectionTime)
                    print "Rejection Time: " + rejection_time
                  except AttributeError:
                    print "Approval/Rejection Time: N/A"
                try:
                  #if(mtime2datetime(mturk_test_time) < mtime2datetime(approval_time)):
                  if(1):
                    a = 0
                    for question_form_answer in assignment.answers[0]:
                        answers[hitcount] = question_form_answer
                        for value in question_form_answer.fields:
                          a += 1
                          print 'field' + str(a) + ': ' + value
                    #print 'work time (s): ' + assignment.WorkTimeInSeconds
                    annotations_struct  = assignment.answers[0][2]
                    annotations_str = annotations_struct.fields[0]
                    annotations = strip_first(annotations_str,'|').split('|')
                    numannotations = len(annotations)
                    #print annotations
                    #print numannotations
                    numwords = len(annotations_str.replace('|',' ').split(' '))
                    #print 'annotations_str: ' + annotations_str
                    #print 'numwords: %d' % numwords
                    #print 'numannotations: %d' % numannotations
                    bonus = floor(max(0,numannotations-5) / 5.0 * 2) / 2.0 * 0.55;
                    #bonus = floor(bonus*2)/2.0
                    print 'bonus: ' + str(bonus)
                    increment_dict(bonuses, assignment.WorkerId, [[assignment.AssignmentId, bonus, (numannotations-5)/5*5]])
                    increment_dict(submit_counts, assignment.WorkerId, 1)
                    increment_dict(annotation_counts, assignment.WorkerId, numannotations)
                    increment_dict(word_counts, assignment.WorkerId, numwords)
                  else:
                    print 'Too old!'
                  print "--------------------"
                except AttributeError:
                  a = 0
                #print words_per_annot
                #print "--------------------"
                #print hit
                #csvwriter.writerow([vidmp4, vidwebm, '', i, i+resolution])

print bonuses
print submit_counts
print annotation_counts

bonus_totals = np.zeros(len(bonuses))

for i in arange(len(bonuses)):
  print "%d - %s:" % (i, bonuses.keys()[i])
  for bonus in bonuses.values()[i]:
    print "%s, %f" % (bonus[0],bonus[1]) ,
    bonus_totals[i] += bonus[1]
  print ''
  print 'total: ' + str(bonus_totals[i])

index = int(raw_input('select worker to pay bonus (-1 for all)'))

if(index == -1):
  for i in arange(len(bonuses)):
    pay_bonuses(bonuses, i)
else:
  pay_bonuses(bonuses,index)
"""
print 'worker %s: approve all assignments and pay %f bonus?' % (bonuses.keys()[index],bonus_totals[index])
answer = raw_input('yes/no: ')
if(answer == 'yes'):
  for bonus in bonuses.values()[index]:
    assignment_id = bonus[0]
    amount = bonus[1]
    if(amount > 0):
      annotation_count = bonus[2]
      reason = 'Extra ' + str(annotation_count) + ' annotations. Thank you very much!'
      #print reason
      pay_bonus(worker_id, assignment_id, amount, reason)
      print 'bonus paid!'
else:
  print 'bonus not paid'
"""
"""
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
"""
"""
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
