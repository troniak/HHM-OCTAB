
#converts mturk output to a similarity matrix and saves in .mat format to local directory

import sys
import time
from matplotlib import pyplot as plt
from numpy import *
import numexpr as ne
import scipy.io as sio
import os
import shutil
from collections import OrderedDict as odict
from lib.agreement_metrics import *
from lib.utils import *
from lib.io_utils import *
output_headers = []
inputs = sys.argv

output_name = inputs[1]
csvreader = init_csv(output_name,'rbU')
rowsIter = iter(csvreader)
output_headers = next(rowsIter)
#print output_headers
rows = [[]]
workerIds = {}
for rowsA in rowsIter:
  rows += [rowsA]
  increment_dict(workerIds,rowsA[output_headers.index('WorkerId')],1)

dummy_similarities    = rows[1][output_headers.index('Answer.similarity')].split('|')
similarity_matrix = zeros(shape=(len(dummy_similarities),len(dummy_similarities)))
#similarity_matrix = []

def calc_for_worker(rows,target_worker):
  sum_similarity_matrix_rows = {}
  count_similarity_matrix_rows = {}
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
      #similarity_matrix+= [similarities]

      if(workerId == target_worker):
        sum_similarity_matrix_row = {}
        for c_file,c_start_time,c_end_time,similarity in zip(c_files,c_start_times,c_end_times,similarities):
          #print (c_file+"|"+str(c_start_time))
          increment_dict(sum_similarity_matrix_row,str(c_end_time-c_start_time),similarity)
        print odict(sorted(sum_similarity_matrix_row.items()))
        sum_similarity_matrix_row_array = odict(sorted(sum_similarity_matrix_row.items())).values()
        increment_dict_elementwise(sum_similarity_matrix_rows,str(r_end_time-r_start_time),sum_similarity_matrix_row_array)
        increment_dict(count_similarity_matrix_rows,str(r_end_time-r_start_time),1)

  #dict to ordered dict:
  sum_similarity_matrix_rows = odict(sorted(sum_similarity_matrix_rows.items()))#.values()
  count_similarity_matrix_rows = odict(sorted(count_similarity_matrix_rows.items()))#.values()
  #mean_similarity_matrix = [divide_array_by_scalar(row, count) for row,count in zip(sum_similarity_matrix_rows,count_similarity_matrix_rows)]
  mean_similarity_matrix = divide_dict_array_elementwise(sum_similarity_matrix_rows,count_similarity_matrix_rows)
  print "WID: " + target_worker
  print "MDM: " ,
  print mean_similarity_matrix
  sio.savemat('output/similarity_matrix_'+target_worker+'.mat', {'mean_similarity_matrix':odict(sorted(mean_similarity_matrix.items())).values()})
  sio.savemat('output/similarity_header_'+target_worker+'.mat', {'mean_similarity_header':odict(sorted(mean_similarity_matrix.items())).keys()})

for workerId in workerIds.keys():
  calc_for_worker(rows, workerId)

"""
mean_similarity_matrix = {}
for key in sum_similarity_matrix_rows.keys():
  mean_similarity_matrix[key] = collections.OrderedDict(sorted(divide_dict(sum_similarity_matrix_rows[key],len(rows)).items())).values()
mean_similarity_matrix = collections.OrderedDict(sorted(mean_similarity_matrix.items())).values()
print mean_similarity_matrix
"""
"""
#matrix = collections.OrderedDict(sorted(similarity_matrix_rows.items()))
matrix = sorted(similarity_matrix_rows.items())
rowcnt = 0
for row in matrix:
  colcnt = 0
  print c_start_times[rowcnt],
  for element in row[1]:
    #print element[1]
    similarity_matrix[rowcnt,colcnt]=element[1]
    colcnt+=1
  rowcnt+=1
print similarity_matrix_rows
#titles = ['mdew_bottle_pick','mdew_bottle_place','soymilk_pick','dressing_packet_pick','salad_box_pick','popcup_pick','pizza_box_pick']
#print ; print titles
"""
