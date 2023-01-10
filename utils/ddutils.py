# return next available node index and update `avail`
# if `avail` is integer return that number
# if `avail` is list return first item
def getNextAvail(avail):
    if type(avail) == int:
        return avail, avail+1
    elif type(avail) == set or type(avail) == list:
        res = avail.pop()
        return res, avail

# set restrictions for an a < b constraint
# return [(clauses)], avail
def compareLess(bits, val, avail):
    if (1 << len(bits)) <= val:
        return [], avail
    lastDpBits, avail = getNextAvail(avail)
    clauses=[(lastDpBits)]
    for i in range(len(bits)-1, -1, -1):
        thisDpBits, avail = getNextAvail(avail)
        # if last <         then this <
        clauses.append((-lastDpBits, thisDpBits))
        if (val >> i) & 1 == 0:
            # if i on           then last < 
            clauses.append((-bits[i], lastDpBits))
            # if last not <     then i not on
            clauses.append((lastDpBits, -bits[i]))
            # if last not <     then this not <
            clauses.append((lastDpBits, -thisDpBits))
        else:
            # if last not < and i on then this not <
            clauses.append((lastDpBits, -bits[i], -thisDpBits))
            # if last not < and i off then this <
            clauses.append((lastDpBits, bits[i], thisDpBits))
        lastDpBits = thisDpBits
    
    return clauses, avail
