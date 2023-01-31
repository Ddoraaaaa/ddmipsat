#!/usr/bin/env python3

import csv
from generators.genConstraints import genXYSet
from utils.ddutils import getSize
from utils.partition import partitionGroups
from copy import deepcopy

def checkTest(n, m, sumQ, numTest, fileName, append, avail):
    origAvail = deepcopy(avail)
    if append == True:
        _mode = 'a'
    else:
        _mode = 'w'
    with open(fileName, mode = _mode) as outFile:
        outStream = csv.writer(outFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)        
        if append == False:
            outStream.writerow(['left_cnt', 'right_cnt', 'original_sum', 'naive_cnt', 'new_cnt', 'saving'])

        for i in range(numTest):
            avail = deepcopy(origAvail)
            xList, yList, yConnected, avail = genXYSet(n, m, sumQ, avail)
            print("hey", yList, avail)
            origSum = getSize(yConnected)
            naiveCnt = origSum - getSize(yList)
            yVals, newDeclare, avail = partitionGroups(yConnected, avail)
            outStream.writerow([n, m, origSum, naiveCnt, len(newDeclare), len(newDeclare)/naiveCnt])



