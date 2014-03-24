from numpy import arange
from numpy import divide
from numpy import array
import numpy as np
import os
import shutil
from matplotlib import pyplot as plt

#strip first in delim-separated string of elements
def strip_first(to_strip,delim):
    first_delim = to_strip.find(delim)
    if(first_delim != -1):
        to_strip = to_strip[first_delim+1:]
    else:
        to_strip = ''
    return to_strip

def increment_dict(diction, key, num_increment):
    if(diction.has_key(key)):
        diction[key] = diction[key] + num_increment
    else:
        diction[key] = num_increment

"""
def append_to_dict(diction, key, value):
    if(diction.has_key(key)):
        diction[key] = diction[key].append(value)
    else:
        diction[key] = [value]
"""

def plot_dict(diction):
    min_frequency = 0.05 * max(diction.values())
    diction = dict((key, frequency) for key, frequency in diction.items() if frequency >= min_frequency)
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

def dict_ratio(d1, d2):
    value_ratio = divide(array(d1.values()), array(d2.values()))
    d3 = {k:v for k,v in zip(d1.keys(),value_ratio)}
    return d3

def url2name(url):
    return url[url.rfind('/')+1:url.rfind('.')]

