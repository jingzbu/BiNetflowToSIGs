#!/usr/bin/env python
""" A library of utility functions
"""
from __future__ import absolute_import, division

__author__ = "Jing Zhang"
__email__ = "jingzbu@gmail.com"
__status__ = "Development"



def readRawData(inputFile):
    """
    Read in the fields of interest from the original raw data file
    """

    tempFile = open(inputFile)

    startTime =[]
    srcAddr = []
    direc = []
    dstAddr = []
    label = []

    for line in tempFile:
        if 'who' in line and 'Botnet' in line:
            print 'Something wrong with the original data!'
            break
        d_1, _, _, d_2, _, d_3, d_4, _, _, _, _, _, _, _, d_5 = line.split(',')
        startTime.append(d_1)
        srcAddr.append(d_2)
        direc.append(d_3)
        dstAddr.append(d_4)
        label.append(d_5)
        print d_1, d_2, d_3, d_4, d_5

    del startTime[0], srcAddr[0], direc[0], dstAddr[0], label[0]

    return startTime, srcAddr, direc, dstAddr, label


def preProcess(raw_data):
    """
    Preprocess the raw data
    """
    startTime, srcAddr, direc, dstAddr, label = readRawData(raw_data)

    assert(len(startTime) == len(srcAddr))
    assert(len(startTime) == len(direc))
    assert(len(startTime) == len(dstAddr))
    assert(len(startTime) == len(label))

    for i in range(len(startTime)):

        # Convert the format of time stamp into pure seconds
        startTime[i] = float(startTime[i].split(' ')[1].split(':')[0]) * (60 ** 2) + \
                       float(startTime[i].split(' ')[1].split(':')[1]) * 60 + \
                       float(startTime[i].split(' ')[1].split(':')[2])

        # Convert the format of direction into single numbers
        if '<' in str(direc[i]) and '>' in str(direc[i]):
            direc[i] = 2
        elif '<' in str(direc[i]):
            direc[i] = -1
        elif '>' in str(direc[i]):
            direc[i] = 1
        # In the original raw data, there exist directions indicated by '  who',
        # meaning we do not know the exact values; however, such netflows are with
        # "background" label, so we can ignore them.
        else:
            direc[i] = 0

        # Convert the format of label into single numbers
        # Set the normal flow label to be '-1'
        if 'Normal' in label[i]:
            label[i] = -1
        # Set the background flow label to be '0'
        elif 'Background' in label[i]:
            label[i] = 0
        # Set the botnet flow label to be '1'
        elif 'Botnet' in label[i]:
            label[i] = 1

        # Preprocess IPs in previously preprocessed data
        # Essentially delete invalid lines (with non-ipv4 IP and non-Botnet label)
        if ':' in srcAddr[i]:
            # Ensure that the line we delete is not with a "Botnet" label
            assert(label[i] != 1)
            srcAddr[i] = '255.255.255.255'
            direc[i] = 0
            dstAddr[i] = '255.255.255.255'

        print startTime[i], srcAddr[i], direc[i], dstAddr[i], label[i]

    assert(direc.count(0) + direc.count(1) + direc.count(-1) + direc.count(2) == len(label))
    assert(label.count(0) + label.count(1) + label.count(-1) == len(label))

    return startTime, srcAddr, direc, dstAddr, label