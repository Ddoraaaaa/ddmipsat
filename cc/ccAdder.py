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

    return clauses, [z0, z1], avail

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

    return clauses, [z0, z1], avail

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
    return clauses, avail
