#!/usr/bin/env python
""" A library of utility functions
"""
from __future__ import absolute_import, division

__author__ = "Jing Zhang"
__email__ = "jingzbu@gmail.com"
__status__ = "Development"


import argparse
import socket

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


class convertBinetflowToSigs:
    def __init__(self, parser):
        self.parser = parser

    def run(self):
        args = self.parser
        win_size = args.w
        data_folder = args.d
        raw_data = args.p
        result = args.s
        # Call the function "preProcess" to preprocess the raw data
        # raw_data = raw_data_folder + 'capture20110816.binetflow'
        startTime, srcAddr, direc, dstAddr, label = preProcess(raw_data)

        setOfSrcAddr = set(srcAddr)
        setOfDstAddr = set(dstAddr)
        setOfIP = setOfSrcAddr.union(setOfDstAddr)

        assert(len(setOfSrcAddr) + len(setOfDstAddr) > len(setOfIP))

        # Sort the IPs
        sortedIPList = sorted(setOfIP, key=socket.inet_aton)

        print sortedIPList
        print '-' * 40

        # Use a dictionary to store the sorted IPs, each with an integer label
        dictIP = dict(zip(sortedIPList, range(0, len(sortedIPList))))

        # N is the number of SIGs to be constructed
        N = int((startTime[len(startTime) - 1] - startTime[0]) // win_size)
        print 'We have %d SIGs.' %N

        # Write SIGs to a standard output file
        sigs = data_folder + result
        with open(sigs, 'w') as sigFile:
            for i in range(len(sortedIPList)):
                sigFile.write(str(sortedIPList[i])+' ')
            sigFile.write('\n')
            for n in range(N):
                print 'The SIG #%d is being constructed.' %n
                sigFile.write('G%d\n' %n)
                listEdges = []
                for i in range(len(startTime)):
                    if startTime[i] >= startTime[0] + n * win_size and \
                                    startTime[i] < startTime[0] + (n + 1) * win_size and \
                                    direc[i] != 0:
                        if direc[i] == 1:
                            listEdges.append('%d -> %d' %(dictIP[srcAddr[i]], dictIP[dstAddr[i]]))
                        if direc[i] == -1:
                            listEdges.append('%d -> %d' %(dictIP[dstAddr[i]], dictIP[srcAddr[i]]))
                        if direc[i] == 2:
                            listEdges.append('%d -> %d' %(dictIP[srcAddr[i]], dictIP[dstAddr[i]]))
                            listEdges.append('%d -> %d' %(dictIP[dstAddr[i]], dictIP[srcAddr[i]]))
                listEdges = list(set(listEdges))
                for j in range(len(listEdges)):
                    edge = listEdges[j]
                    print edge
                    sigFile.write(edge)
                    sigFile.write('\n')