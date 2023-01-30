from .ddutils import getNextAvail
from collections import defaultdict as dd

def removeVal(cntPair, groups, val):
    for group in groups:
        if val not in group:
            continue
        group.remove(val)
        for val1 in group:
            cntPair[(min(val, val1), max(val, val1))] -= 1

def addVal(cntPair, groups, val, toAdd):
    for i in toAdd:
        group = groups[i]
        for val1 in group:
            cntPair[(min(val, val1), max(val, val1))] += 1
        group.append(val)


def partitionGroups(groups, avail):
    resList = []
    cntPair = dd(lambda: 0)
    # initial count
    for group in groups:
        for idx, a in enumerate(group):
            for b in groups[idx + 1:]:
                cntPair[(min(a, b), max(a, b))] += 1

    while True:
        (u, v) = max(cntPair, key=cntPair.get)
        if cntPair[(u, v)] == 0:
            break
        newVal, avail = getNextAvail(avail)

        resList.append((newVal, u, v))

        toAdd = []
        for idx, group in enumerate(groups):
            if u in group:
                toAdd.append(idx)

        removeVal(cntPair, groups, u)
        removeVal(cntPair, groups, v)

        addVal(cntPair, groups, newVal, toAdd)

    return [group[0] for group in groups], resList