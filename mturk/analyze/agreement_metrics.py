from numpy import *
from matplotlib import pyplot as plt

def calc_annotation_agreement(As, Ae, Bs, Be,epsilon,fps,max_time,vid_start_time):
  #print As
  #print Ae
  #print Bs
  #print Be
  agreement_matrix = zeros(shape=(max_time*fps,max_time*fps))
  agreed = 0
  #print vid_start_time
  for sA,eA in zip(As,Ae):
    for sB,eB in zip(Bs,Be):
      sdiff = round(sA*fps) - round(sB*fps)
      ediff = round(eA*fps) - round(eB*fps)
      if(abs(sdiff) <= epsilon and abs(ediff) <= epsilon):
      #if((round(sA*fps) == round(sB*fps)) and round(eA*fps) == round(eB*fps)):
        #print abs(round(sA*fps) - round(sB*fps))
        #print abs(round(eA*fps) - round(eB*fps))
        #print 'agreed!'
        #print int(round((vid_start_time+sA)*fps))
        #print int(round((vid_start_time+sB)*fps))
        #print int(round((vid_start_time+eA)*fps))
        #print int(round((vid_start_time+eB)*fps))
        adiff = max(abs(sdiff),abs(ediff))+1
        agreed = 1
        agreement_matrix[int(round((vid_start_time+sA)*fps)+sdiff),int(round((vid_start_time+eA)*fps)+ediff)] += (1.0/adiff)
        #plt.imshow(agreement_matrix)
        #plt.show()
  #print agreement_matrix
  if(agreed):
    return agreement_matrix
  else:
    return None

def calc_event_agreement(As, Ae, Bs, Be):
    agreed_event_counter = 0.0
    identified_counter = len(As) + len(Bs)
    for sA,eA in zip(As,Ae):
        agree_counted = 0
        for sB,eB in zip(Bs,Be):
            if(not agree_counted and ((sA >= sB and sA <= eB) or (eA <= eB and eA >= sB))):
                #print str(sA) + '<->' + str(eA)
                #print str(sB) + '<->' + str(eB)
                agreed_event_counter += 1.0
                agree_counted = 1
    for sB,eB in zip(Bs,Be):
        agree_counted = 0
        for sA,eA in zip(As,Ae):
            if(not agree_counted and ((sB >= sA and sB <= eA) or (eB <= eA and eB >= sA))):
                agreed_event_counter += 1.0
                agree_counted = 1
    return agreed_event_counter / identified_counter

def calc_segmentation_agreement(As, Ae, Bs, Be):
    agreed_slice_counter = 0.0
    slice_counter = 0.0

    for i in arange(1,max(max(Ae),max(Be))):
        noagree_counted = 0
        for sA,eA in zip(As,Ae):
            for sB,eB in zip(Bs,Be):
                if((sA >= sB and sA <= eB) or (eA <= eB and eA >= sB)):
                    if((i >= sA and i <= eA) and (i >= sB and i <= eB)):
                        agreed_slice_counter += 1
                        #print str(i)+':['+str(sA)+'|'+str(eA)+'],['+str(sB)+'|'+str(eB)+']=agree'
                    elif(not noagree_counted and ((i >= sA and i <= eA) or (i >= sB and i <= eB))):
                        slice_counter += 1
                        noagree_counted = 1
                        #print str(i)+':['+str(sA)+'|'+str(eA)+'],['+str(sB)+'|'+str(eB)+']=noagree'
    return agreed_slice_counter / float(slice_counter)

'''
Python implementation of Krippendorff's alpha -- inter-rater reliability

(c)2011 Thomas Grill (http://grrrr.org)
license: http://creativecommons.org/licenses/by-sa/3.0/

Python version >= 2.4 required
'''

try:
    import numpy as N
except ImportError:
    N = None

def nominal_metric(a,b):
    return a != b

def interval_metric(a,b):
    return (a-b)**2

def ratio_metric(a,b):
    return ((a-b)/(a+b))**2

def krippendorff_alpha(data,metric=interval_metric,force_vecmath=False,convert_items=float,missing_items=None):
    '''
    Calculate Krippendorff's alpha (inter-rater reliability):

    data is in the format
    [
        {unit1:value, unit2:value, ...},  # coder 1
        {unit1:value, unit3:value, ...},   # coder 2
        ...                            # more coders
    ]
    or
    it is a sequence of (masked) sequences (list, numpy.array, numpy.ma.array, e.g.) with rows corresponding to coders and columns to items

    metric: function calculating the pairwise distance
    force_vecmath: force vector math for custom metrics (numpy required)
    convert_items: function for the type conversion of items (default: float)
    missing_items: indicator for missing items (default: None)
    '''


    # number of coders
    m = len(data)

    # set of constants identifying missing values
    maskitems = set((missing_items,))
    if N is not None:
        maskitems.add(N.ma.masked_singleton)

    # convert input data to a dict of items
    units = {}
    for d in data:
        try:
            # try if d behaves as a dict
            diter = d.iteritems()
        except AttributeError:
            # sequence assumed for d
            diter = enumerate(d)

        for it,g in diter:
            if g not in maskitems:
                try:
                    its = units[it]
                except KeyError:
                    its = []
                    units[it] = its
                its.append(convert_items(g))


    units = dict((it,d) for it,d in units.iteritems() if len(d) > 1)  # units with pairable values
    n = sum(len(pv) for pv in units.itervalues())  # number of pairable values

    N_metric = (N is not None) and ((metric in (interval_metric,nominal_metric,ratio_metric)) or force_vecmath)

    Do = 0.
    for grades in units.itervalues():
        if N_metric:
            gr = N.array(grades)
            Du = sum(N.sum(metric(gr,gri)) for gri in gr)
        else:
            Du = sum(metric(gi,gj) for gi in grades for gj in grades)
        Do += Du/float(len(grades)-1)
    Do /= float(n)
    #print 'Do: %f'%Do

    De = 0.
    for g1 in units.itervalues():
        if N_metric:
            d1 = N.array(g1)
            for g2 in units.itervalues():
                De += sum(N.sum(metric(d1,gj)) for gj in g2)
        else:
            for g2 in units.itervalues():
                De += sum(metric(gi,gj) for gi in g1 for gj in g2)
    De /= float(n*(n-1))
    #print 'De: %f'%De

    return 1.-Do/De

