#! /usr/bin/env python

def readIntercalibration(filename, ic):

    #read intercalibrations
    f = open(filename)
    for line in f:
        if ('Expander' in line): continue
        #print line.replace('\n','').split(' ')
        ie, it, dt =  line.replace('\n','').split(' ')
        #print ie, it, dt 
        ic[int(ie)][int(it)] = float(dt)
        
    return
