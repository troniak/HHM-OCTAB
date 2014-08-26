import os
import csv

def init_file(filename,mode):
    open(filename, mode).close() #properly closed if dangling
    f = open(filename, mode)
    return f

def init_csv(filename,mode):
    name, extension = os.path.splitext(filename)
    print name
    open(name+'.csv', mode).close()
    csvfile = open(name+'.csv', mode)
    if('w' in mode):
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(headers)
        return csvwriter
    elif('r' in mode):
        csvreader = csv.reader(csvfile, delimiter=',')
        return csvreader

def mkdir(dir_name):
    try:
        os.mkdir(dir_name)
    except OSError:
        print 'dir ' + dir_name + ' already exists'
