
#converts mturk output to a distance matrix and saves in .mat format to local directory

import sys
import time
from matplotlib import pyplot as plt
from numpy import *
import numexpr as ne
from agreement_metrics import *
from utils import *
from io_utils import *
import scipy.io as sio
import os
import shutil
from collections import OrderedDict as odict
output_headers = []
inputs = sys.argv

def increment_dict(diction, key, num_increment):
    if(diction.has_key(key)):
        diction[key] = diction[key] + num_increment
    else:
        diction[key] = num_increment

def increment_dict_elementwise(diction, key, array_increment):
    if(diction.has_key(key)):
        diction[key] = [sum(x) for x in zip(diction[key], array_increment)]
    else:
        diction[key] = array_increment

def divide_dict_elementwise(d1,d2):
  d3 = dict((k, float(d1[k]) / float(d2[k])) for k in d2)
  return d3
def divide_dict(d1,n):
  d3 = dict((k, float(d1[k]) / float(n)) for k in d1)
  return d3

def divide_array_by_scalar(a,s):
  a2 = [float(k) / float(s) for k in a]
  return a2

output_name = inputs[1]
if(os.path.isfile('/Users/troniak/Downloads/'+output_name+'.csv')):
  shutil.move('/Users/troniak/Downloads/'+output_name+'.csv', '../output/'+output_name+'.csv')
csvreader = init_csv('../output/'+output_name,'rb')
rowsIter = iter(csvreader)
output_headers = next(rowsIter)
#print output_headers
rows = [[]]
for rowsA in rowsIter:
  rows += [rowsA]

dummy_similarities    = rows[1][output_headers.index('Answer.similarity')].split('|')
distance_matrix = zeros(shape=(len(dummy_similarities),len(dummy_similarities)))
#distance_matrix = []

sum_distance_matrix_rows = {}
count_distance_matrix_rows = {}
count_matrix_row = {}
for row in rows:
  if(len(row) > 0):
    hitId           = row[output_headers.index('HITId')]
    workerId        = row[output_headers.index('WorkerId')]
    status          = row[output_headers.index('AssignmentStatus')]
    file_reference  = row[output_headers.index('Input.file_reference')]
    r_start_time    = float(row[output_headers.index('Input.reference_start_time')])
    r_end_time      = float(row[output_headers.index('Input.reference_end_time')])
    c_files         = row[output_headers.index('Input.files_tocompare')].split('|')
    c_start_times   = [float(s) for s in row[output_headers.index('Input.tocompare_start_times')].split('|')]
    c_end_times     = [float(s) for s in row[output_headers.index('Input.tocompare_end_times')].split('|')]
    similarities    = [int(s) for s in row[output_headers.index('Answer.similarity')].split('|')]
    #distance_matrix+= [similarities]

    sum_distance_matrix_row = {}
    for c_file,c_start_time,c_end_time,similarity in zip(c_files,c_start_times,c_end_times,similarities):
      increment_dict(sum_distance_matrix_row,c_start_time,similarity)
    sum_distance_matrix_row_array = odict(sorted(sum_distance_matrix_row.items())).values()
    increment_dict_elementwise(sum_distance_matrix_rows,r_start_time,sum_distance_matrix_row_array)
    increment_dict(count_distance_matrix_rows,r_start_time,1)

#dict to sorted array:
sum_distance_matrix_rows = odict(sorted(sum_distance_matrix_rows.items())).values()
count_distance_matrix_rows = odict(sorted(count_distance_matrix_rows.items())).values()
mean_distance_matrix = [divide_array_by_scalar(row, count) for row,count in zip(sum_distance_matrix_rows,count_distance_matrix_rows)]
sio.savemat('similarity_matrix.mat', {'mean_distance_matrix':mean_distance_matrix})

"""
mean_distance_matrix = {}
for key in sum_distance_matrix_rows.keys():
  mean_distance_matrix[key] = collections.OrderedDict(sorted(divide_dict(sum_distance_matrix_rows[key],len(rows)).items())).values()
mean_distance_matrix = collections.OrderedDict(sorted(mean_distance_matrix.items())).values()
print mean_distance_matrix
"""
"""
#matrix = collections.OrderedDict(sorted(distance_matrix_rows.items()))
matrix = sorted(distance_matrix_rows.items())
rowcnt = 0
for row in matrix:
  colcnt = 0
  print c_start_times[rowcnt],
  for element in row[1]:
    #print element[1]
    distance_matrix[rowcnt,colcnt]=element[1]
    colcnt+=1
  rowcnt+=1
print distance_matrix_rows
#titles = ['mdew_bottle_pick','mdew_bottle_place','soymilk_pick','dressing_packet_pick','salad_box_pick','popcup_pick','pizza_box_pick']
#print ; print titles
"""
