import os
import csv

def init_file(name,mode):
    open(name, mode).close()
    f = open(name, mode)
    return f

def init_csv(name,mode):
    open(name+'.csv', mode).close()
    csvfile = open(name+'.csv', mode)
    if(mode == 'wb'):
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(headers)
        return csvwriter
    elif(mode == 'rb'):
        csvreader = csv.reader(csvfile, delimiter=',')
        return csvreader

def mkdir(dir_name):
    try:
        os.mkdir(dir_name)
    except OSError:
        print 'dir ' + dir_name + ' already exists'
