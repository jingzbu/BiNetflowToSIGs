#!/usr/bin/env python
""" Main classes functions
"""
from __future__ import absolute_import, division

__author__ = "Jing Zhang"
__email__ = "jingzbu@gmail.com"
__status__ = "Development"


from ..util.util import *
import socket



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

        print(sortedIPList)
        print('-' * 40)

        # Use a dictionary to store the sorted IPs, each with an integer label
        dictIP = dict(zip(sortedIPList, range(0, len(sortedIPList))))

        # Assign label to each node (IP)


        # N is the number of SIGs to be constructed
        N = int((startTime[len(startTime) - 1] - startTime[0]) // win_size)
        print('We have %d SIGs.' %N)

        # Write SIGs to a standard output file
        sigs = data_folder + result
        with open(sigs, 'w') as sigFile:
            for i in range(len(sortedIPList)):
                sigFile.write(str(sortedIPList[i])+' ')
            sigFile.write('\n')
            for n in range(N):
                print('The SIG #%d is being constructed.' %n)
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
                    print(edge)
                    sigFile.write(edge)
                    sigFile.write('\n')