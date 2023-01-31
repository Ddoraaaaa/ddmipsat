#!/usr/bin/env python3

from collections import defaultdict
from random import randint, shuffle
from math import floor
from utils.ddutils import getNextAvail

def getSizes(n, m, sumQ):
    res = []
    if sumQ == 0:
        res = [randint(1, n) for i in range(m)]
    else:
        res = [floor(sumQ / m) + (1 if i < sumQ % m else 0) for i in range(m)]
    return res


def genXYSet(n, m, sumQ, avail):
    sumQ = min(sumQ, n * m)
    xList = []
    yList = []
    yConnected = []
    ySizeList = getSizes(n, m, sumQ)

    for i in range(n):
        newId, avail = getNextAvail(avail)
        xList.append(newId)

    for i in range(m):
        newId, avail = getNextAvail(avail)
        yList.append(newId)
        shuffle(xList)
        yConnected.append(xList[0:ySizeList[i]])

    return xList, yList, yConnected, avail

    




    
    