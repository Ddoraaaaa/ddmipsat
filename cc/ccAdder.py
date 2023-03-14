from ..utils.ddutils import getNextAvail, compareLess

# half adder for 2 bits
# return [(clauses)], [z0, 2z1], avail
def ccHalfAdder2(bits, avail):
    z0, avail = getNextAvail(avail)
    z1, avail = getNextAvail(avail)

    clauses = []

    b0, b1 = bits

    clauses.append((b0, b1, -z0))
    clauses.append((-b0, -b1, -z0))
    clauses.append((b0, -b1, z0))
    clauses.append((-b0, b1, z0))

    clauses.append((-b0, -b1, z1))
    clauses.append((b0, -z1))
    clauses.append((b1, -z1))

    return clauses, z0, z1, avail

# half adder for 2 bits, into z0 + 2z1 >= x1 + x2
# return [(clauses)], [z0, 2z1], avail
def ccHalfAdder2Loose(x1, x2, avail):
    z1, avail = getNextAvail(avail)
    z0, avail = getNextAvail(avail)
    clauses = [
        (-x1, -x2, z1),
        (-x1, x2, z0),
        (x1, -x2, z0)
    ]
    return clauses, z0, z1, avail

# full adder for 3 bits, into z0 + 2z1
# return [(clauses)], [z0, 2z1], avail
def ccFullAdder3(bits, avail):
    z0, avail = getNextAvail(avail)
    z1, avail = getNextAvail(avail)
    clauses = []
    
    b0, b1, b2 = bits

    clauses.append((-b0, -b1, -b2, z0))
    clauses.append((b0, b1, b2, -z0))
    
    clauses.append((-b0, -b1, b2, -z0))
    clauses.append((-b0, b1, -b2, -z0))
    clauses.append((b0, -b1, -b2, -z0))

    clauses.append((-b0, b1, b2, z0))
    clauses.append((b0, b1, -b2, z0))
    clauses.append((b0, -b1, b2, z0))

    clauses.append((-b0, -b1, z1))
    clauses.append((-b0, -b2, z1))
    clauses.append((-b1, -b2, z1))

    clauses.append((b0, b1, -z1))
    clauses.append((b0, b2, -z1))
    clauses.append((b1, b2, -z1))

    return clauses, z0, z1, avail

# full adder for 3 bits, into z0 + 2z1 >= val
# return [(clauses)], [z0, 2z1], avail
def ccFullAdder3Loose(x1, x2, x3, avail):
    z1, avail = getNextAvail(avail)
    z0, avail = getNextAvail(avail)
    temp, avail = getNextAvail(avail)
    clauses = [
        (-x1, -x2, z1),
        (-x1, -x3, z1),
        (-x2, -x3, z1),
        (-x1, -z1, z0),
        (-x2, -z1, z0),
        (-x3, -z1, z0),
        (-x1, -x2, temp),
        (-temp, -x3, z0)
    ]
    return clauses, z0, z1, avail

# expression in the form of [x1, x2, ..., xn]
# return [(clauses)], [z0, 2z1, ...], avail
def ccEncodeExpression(expression, avail):
    if len(expression) == 2:
        return ccHalfAdder2(expression, avail)
    if len(expression) == 3:
        return ccFullAdder3(expression, avail)

    lHalf = expression[:len(expression)/2]
    rHalf = expression[len(expression)/2:]

    clauses, lBits, avail = ccEncodeExpression(lHalf, avail)
    tempClauses, rBits, avail = ccEncodeExpression(rHalf, avail)
    clauses.extend(tempClauses)

    resBits = []
    for i in range(len(rBits)):
        if i == 0:
            tempClauses, tempBits, avail = ccHalfAdder2(lBits[i], rBits[i], avail)
            clauses.extend(tempClauses)
            resBits.append(tempBits[0]) 
            carry = tempBits[1]
        elif i == len(rBits):
            tempClauses, tempBits, avail = ccHalfAdder2(rBits[i], carry, avail)
            clauses.extend(tempClauses)
            resBits.append(tempBits[0]) 
            carry = tempBits[1]
        else:            
            tempClauses, tempBits, avail = ccFullAdder3(lBits[i], rBits[i], carry, avail)
            clauses.extend(tempClauses)
            resBits.append(tempBits[0]) 
            carry = tempBits[1]

    resBits.append(carry)
    return clauses, resBits, avail

def ccComparison(k, x, avail):
    # Check if largest bit of x is more than nth position
    if x >= 2**len(k):
        return [], avail
    
    # Get list of indexes
    e = []
    for _ in range(len(k) + 2):
        temp, avail = getNextAvail(avail)
        e.append(temp)
    
    # Initialize list of clauses
    clauses = [[e[-1]]]
    
    # Iterate through each position i from n to 1
    for i in range(len(k), 0, -1):
        # Append [-ei, ei+1] to clauses
        clauses.append([-e[i], e[i+1]])
        
        # If ith bit of x is 0, append [-ki, -ei+1] to clauses
        if x & (1 << (i-1)) == 0:
            clauses.append([-k[i-1], -e[i+1]])
        
        # If ith bit of x is 1, append [-ki, -ei] to clause
        else:
            clauses.append([-k[i-1], -e[i]])
    
    return clauses, avail

# expression in the form of [x1, x2, ..., xn]
# return [(clauses)], [z0, 2z1, ...], avail
def ccEncodeConstraint(constraint, avail):
    expression, sign, value = constraint
    if len(expression) == 2:
        return ccHalfAdder2(expression, avail)
    if len(expression) == 3:
        return ccFullAdder3(expression, avail)

    lHalf = expression[:len(expression)/2]
    rHalf = expression[len(expression)/2:]

    clauses, lBits, avail = ccEncodeExpression(lHalf, avail)
    tempClauses, rBits, avail = ccEncodeExpression(rHalf, avail)
    clauses.extend(tempClauses)

    resBits = []
    for i in range(len(rBits)):
        if i == 0:
            tempClauses, tempBits, avail = ccHalfAdder2(lBits[i], rBits[i], avail)
            clauses.extend(tempClauses)
            resBits.append(tempBits[0]) 
            carry = tempBits[1]
        elif i == len(rBits):
            tempClauses, tempBits, avail = ccHalfAdder2(rBits[i], carry, avail)
            clauses.extend(tempClauses)
            resBits.append(tempBits[0]) 
            carry = tempBits[1]
        else:            
            tempClauses, tempBits, avail = ccFullAdder3(lBits[i], rBits[i], carry, avail)
            clauses.extend(tempClauses)
            resBits.append(tempBits[0]) 
            carry = tempBits[1]

    resBits.append(carry)
    tempClauses, avail = compareLess(resBits, value)

    clauses.extend(tempClauses)
    return clauses, resBits, avail

def ccAddBits(bitlist, avail):
    K = [bitlist]
    clauses = []
    answer = []

    i = 0
    while True:
        if len(K[i]) >= 3:
            x1, x2, x3 = K[i][:3]
            K[i] = K[i][3:]
            fa_clauses, z0, z1 = ccFullAdder3(x1, x2, x3, avail)
            clauses += fa_clauses
            K[i] = [z0] + K[i]
            if i + 1 >= len(K):
                K.append([z1])
            else:
                K[i+1] = [z1] + K[i+1]
        elif len(K[i]) == 2:
            x1, x2 = K[i][:2]
            K[i] = K[i][2:]
            ha_clauses, z0, z1, avail = ccHalfAdder2(x1, x2, avail)
            clauses += ha_clauses
            K[i] = [z0] + K[i]
            if i + 1 >= len(K):
                K.append([z1])
            else:
                K[i+1] = [z1] + K[i+1]
        elif len(K[i]) == 1:
            answer.append(K[i][0])
            if i + 1 < len(K):
                K[i+1].append(0)
            break

        i += 1

    return answer, clauses

def ccAddBitsLoose(bitlist, avail):
    K = [bitlist]
    clauses = []
    answer = []

    i = 0
    while True:
        if len(K[i]) >= 3:
            x1, x2, x3 = K[i][:3]
            K[i] = K[i][3:]
            fa_clauses, z0, z1, avail = ccFullAdder3Loose(x1, x2, x3, avail)
            clauses += fa_clauses
            K[i] = [z0] + K[i]
            if i + 1 >= len(K):
                K.append([z1])
            else:
                K[i+1] = [z1] + K[i+1]
        elif len(K[i]) == 2:
            x1, x2 = K[i][:2]
            K[i] = K[i][2:]
            ha_clauses, z0, z1, avail = ccHalfAdder2Loose(x1, x2, avail)
            clauses += ha_clauses
            K[i] = [z0] + K[i]
            if i + 1 >= len(K):
                K.append([z1])
            else:
                K[i+1] = [z1] + K[i+1]
        elif len(K[i]) == 1:
            answer.append(K[i][0])
            if i + 1 < len(K):
                K[i+1].append(0)
            break

        i += 1

    return answer, clauses, avail
