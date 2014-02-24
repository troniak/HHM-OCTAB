import boto.mturk.connection as conn
from pprint import pprint
from math import *
import csv
import sys
from numpy import arange

headers = ['HITId', 'WorkerID','Input.title','Input.start_time','Input.end_time','Answer.endTimeList','Answer.noMoreActions','Answer.startTimeList']
HIT_headers = ['HITId', 'HITTypeId', 'Title', 'Description', 'Keywords', 'Reward', 'CreationTime', 'MaxAssignments', 'RequesterAnnotation', 'AssignmentDurationInSeconds', 'AutoApprovalDelayInSeconds', 'Expiration', 'NumberOfSimilarHITs', 'LifetimeInSeconds', 'AssignmentId', 'WorkerId', 'AssignmentStatus', 'AcceptTime', 'SubmitTime', 'AutoApprovalTime', 'ApprovalTime', 'RejectionTime', 'RequesterFeedback', 'WorkTimeInSeconds', 'LifetimeApprovalRate', 'Last30DaysApprovalRate', 'Last7DaysApprovalRate', 'Input.video_url_mp4', 'Input.video_url_webm', 'Input.title', 'Input.start_time', 'Input.end_time', 'Answer.annotationText', 'Answer.endTimeList', 'Answer.noMoreActions', 'Answer.startTimeList', 'Approve', 'Reject']

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

mturk = conn.MTurkConnection(aws_access_key_id='AKIAJUL53VTH3ENYMNIQ', aws_secret_access_key='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', is_secure=True, port=None, proxy=None, proxy_port=None, proxy_user=None, proxy_pass=None, host=None, debug=0, https_connection_factory=None, security_token=None, profile_name=None)
#hits = mturk.get_all_hits()
bonuses = {}
hits = mturk.get_all_hits()
print 'Fetching assignments...'
csvwriter_all = init_csv(''+'results','w')
#output_headers = []
for hit in hits:
    #output_headers += [hit.HITId]
    #output_headers += [hit.WorkerID]
    headers = ['HITId', 'WorkerID','Input.title','Input.start_time','Input.end_time','Answer.endTimeList','Answer.noMoreActions','Answer.startTimeList']
    assignments = mturk.get_assignments(hit.HITId)
    for assignment in assignments:
        if(assignment.AssignmentStatus == 'Submitted'):
            print "Answers of the worker %s" % assignment.WorkerId
            for question_form_answer in assignment.answers[0]:
                for value in question_form_answer.fields:
                    print value
            #print 'work time (s): ' + assignment.WorkTimeInSeconds
            question_form_answer = assignment.answers[0][0]
            value = question_form_answer.fields[0]
            bonus = max(0,len(value.split('|'))-5) / 5.0 * 0.5;
            bonus = floor(bonus*2)/2.0
            print 'bonus: ' + str(bonus)
            increment_dict(bonuses, assignment.WorkerId, bonus)
            print "--------------------"
            #print hit
            #csvwriter.writerow([vidmp4, vidwebm, '', i, i+resolution])
print bonuses
print 'Done!'
