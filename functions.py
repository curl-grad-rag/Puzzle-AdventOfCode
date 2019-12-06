def convert2fuel(number):
    """Fuel = floor(number/3) - 2"""
    return max(0, int(number / 3) - 2)

def dat2numarr(fileName):
    """Read data file and return numbers. Ignores non-convertibles"""
    retarr = []
    with open(fileName) as fh:
        for line in fh:
            try:
                num = float(line.lower().rstrip().lstrip())
                if int(num) == num:
                    num = int(num)
                retarr.append(num)
            except ValueError:
                pass
    return retarr

def findTotFuel(number):
    retnum = convert2fuel(number)
    if retnum < 1:
        return retnum
    else:
        return retnum + findTotFuel(retnum)


#print(dat2numarr('c:/Users/rjjumade/Personal/My Codes/Advent2019/day1.dat'))


def intcode(numarrr):
    """
    1st number : operator :: 1-add, 2-mult, 99-halt, else-error
    2nd number : location of first operand
    3rd number : location of second operand
    4th number : location of result
    """
    i = 0
    while i < len(numarrr):
        increment = 4
        if numarrr[i] == 1:
            numarrr[numarrr[i+3]] = numarrr[numarrr[i+1]] + numarrr[numarrr[i+2]]
        elif numarrr[i] == 2:
            numarrr[numarrr[i+3]] = numarrr[numarrr[i+1]] * numarrr[numarrr[i+2]]
        elif numarrr[i] == 99:
            i += 1
            break
        else:
            print("Unknown operator : {}".format(numarrr[i]))
            break
        i += increment

# a = [1,0,0,0,99]
# print(a)
# intcode(a)
# print(a)
# print()
# a = [2,3,0,3,99]
# print(a)
# intcode(a)
# print(a)
# print()
# a = [2,4,4,5,99,0]
# print(a)
# intcode(a)
# print(a)
# print()
# a = [1,1,1,4,99,5,6,0,99]
# print(a)
# intcode(a)
# print(a)
# print()
# a = [1,9,10,3,2,3,11,0,99,30,40,50]
# print(a)
# intcode(a)
# print(a)
# print()

def updateCoordLists(modList, extendList, displacement, dirMult=1, coordSpace=1):
    if dirMult > 0:
        dirMult = 1
    elif dirMult < 0:
        dirMult = -1
    for _ in range(abs(displacement)):
        modList.append(modList[-1] + 1*dirMult*coordSpace)
        extendList.append(extendList[-1])

def obtainPath(instrArr, startX=None, startY=None):
    """
    Converts sequence of traverse instructions to coordinates of path
    eg: instrArr = R2,U2,L2 with start (0,0) produces (0,0), (1,0), (2,0), (2,1), (2,2), (1,2), (0,2)
    """
    listX = []
    listY = []
    if (startX):
        listX.append(startX)
    else:
        listX.append(0)
    
    if (startY):
        listY.append(startY)
    else:
        listY.append(0)
    
    for instr in instrArr:
        displacement = 0
        try:
            displacement = int(instr.lstrip().rstrip()[1:])
        except ValueError:
            print("Ignoring instruction: {}".format(instr))
            continue

        if (instr.lstrip().upper().startswith("R")):
            updateCoordLists(listX, listY, displacement)
        elif (instr.lstrip().upper().startswith("U")):
            updateCoordLists(listY, listX, displacement)
        elif (instr.lstrip().upper().startswith("L")):
            updateCoordLists(listX, listY, displacement, -1)
        elif (instr.lstrip().upper().startswith("D")):
            updateCoordLists(listY, listX, displacement, -1)
    
    listXY = list(zip(listX, listY))
    return listX, listY, listXY

# a, b, c = obtainPath(["R8","U5","L5","D3"])
# print(c)
def findPossiblePass(low, high):
    validOpts = []
    for num in range(low, high):
        digits = [int(x) for x in str(num)]
        prev = 10
        adjCheck = False
        mono_inc = True
        while (digits):
            curr = digits.pop()
            if (curr > prev):
                mono_inc = False
                break
            elif (curr == prev):
                adjCheck = True
            prev = curr
        if (adjCheck and mono_inc):
            validOpts.append(num)
    return validOpts

def reducePassPossibilities(validOpts):
    validOptsRed = []
    for num in validOpts:
        digits = [int(x) for x in str(num)]
        largeGroup = False
        for curr in set(digits):
            if digits.count(curr) == 2:
                largeGroup = True
                break
        if (largeGroup):
            validOptsRed.append(num)
    return validOptsRed


###
def getOperand(numarr, n, mode=0):
    if mode == 0:
        return numarr[n]
    else:
        return n

def enhancedIntCode(numarr, i=0):
    increment = {1:4, 2:4, 3:2, 4:2, 5:3, 6:3, 7:4, 8:4, 99:1}
    while i < len(numarr):
        opcode = numarr[i]
        operand1Mode = int(opcode / 1000) 
        opcode = opcode % 1000
        operand0Mode = int(opcode / 100)
        opcode = opcode % 100
        # print("RJJ: i={}, opcode={}".format(i, opcode))
        if (opcode == 1):
            numarr[numarr[i+3]] = getOperand(numarr, numarr[i+1], operand0Mode) + getOperand(numarr, numarr[i+2], operand1Mode)
        elif (opcode == 2):
            numarr[numarr[i+3]] = getOperand(numarr, numarr[i+1], operand0Mode) * getOperand(numarr, numarr[i+2], operand1Mode)
        elif (opcode == 3):
            numarr[numarr[i+1]] = int(input("Input an integer: "))
        elif (opcode == 4):
            print("Output@i={}: {}".format(i, getOperand(numarr, numarr[i+1], operand0Mode)))
        elif (opcode == 5):
            if getOperand(numarr, numarr[i+1], operand0Mode) != 0:
                i = getOperand(numarr, numarr[i+2], operand1Mode)
                continue
        elif (opcode == 6):
            if getOperand(numarr, numarr[i+1], operand0Mode) == 0:
                i = getOperand(numarr, numarr[i+2], operand1Mode)
                continue
        elif (opcode == 7):
            if getOperand(numarr, numarr[i+1], operand0Mode) < getOperand(numarr, numarr[i+2], operand1Mode):
                numarr[numarr[i+3]] = 1
            else:
                numarr[numarr[i+3]] = 0
        elif (opcode == 8):
            if getOperand(numarr, numarr[i+1], operand0Mode) == getOperand(numarr, numarr[i+2], operand1Mode):
                numarr[numarr[i+3]] = 1
            else:
                numarr[numarr[i+3]] = 0
        elif (opcode == 99):
            break
        else:
            print("Unknown opcode : {}".format(numarr[i]))
            break
        i += increment[opcode]

# enhancedIntCode([3,0,4,0,99])
# enhancedIntCode([1002,4,3,4,33])
# for _ in range(5):
#     inp_code = [3,9,8,9,10,9,4,9,99,-1,8]
#     enhancedIntCode(inp_code)
#     inp_code = [3,9,7,9,10,9,4,9,99,-1,8]
#     enhancedIntCode(inp_code)
#     inp_code = [3,3,1108,-1,8,3,4,3,99]
#     enhancedIntCode(inp_code)
#     inp_code = [3,3,1107,-1,8,3,4,3,99]
#     enhancedIntCode(inp_code)
# inp_code = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
# 1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
# 999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
# enhancedIntCode(inp_code)