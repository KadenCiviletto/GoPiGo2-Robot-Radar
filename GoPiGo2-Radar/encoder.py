from gopigo import *

ticksMultiplier = 20
#this was 20, just changed for testing purposes
leftTicks = [0.0, 0.0]
rightTicks = [0.0, 0.0]
leftDist = [0.0,0.0]
rightDist = [0.0,0.0]
global leftPrev
#global lastfortesting
#lastfortesting = 0
leftPrev = 0
global lastCall
lastCall = 0
global rightPrev
rightPrev = 0
global dist
dist = 0
global leftTemp
leftTemp = 0
global rightTemp
global relativeAngle
global distIndex
distIndex = 0
relativeAngle = 90.0
rightTemp = 0
a = 0
b = 0
global Rotation
rotation = 0

def purge():
    leftTicks = []
    rightTicks = []
    leftDist = []
    rightDist = []
    
def get_left_enc():
    return enc_read(0)

def get_right_enc():
    return enc_read(1)

def get_from_left(l):
    x = leftTicks[l]
    return x

def get_from_right(r):
    r = rightTicks[r]
    return r

def enc_data_write(dir):
        global dist
        a = (get_left_enc() - getLeftPrev())
        leftTicks.append(a)
        b = (get_right_enc() - getRightPrev())
        rightTicks.append(b)
        leftTemp = get_left_enc()
        rightTemp = get_right_enc()
        assignPrev()
        if(dir == 4):
            lastCall = 4
            leftDist.append(a*1.1344)
            rightDist.append(b*1.1344)
            #print("moving forward, dist added: {} {}".format(a,b))
            dist += (b*1.1344)
            updateAngle()
        if(dir == 5):
            lastCall = 5
            updateAngleLeft()
        if(dir == 7):
            lastCall = 7
            updateAngleRight()
        if(dir == 6):
            lastCall = 6
            leftDist.append((-1)*(a*1.1344))
            rightDist.append((-1)*(b*1.1344))
            dist -= (b*1.1344)
            updateAngleRev()

def get_size_arr():
    return len(leftTicks)

def returnleft():
    return leftTicks

def returnright():
    return rightTicks

def getleft():
    return leftTicks

def getright():
    return rightTicks

def assignPrev():
    global leftPrev
    leftPrev = get_left_enc()
    global rightPrev
    rightPrev = get_right_enc()

def getLeftPrev():
    return leftPrev

def getRightPrev():
    return rightPrev

def updateAngle():
    global rotation
    if ( leftTicks[get_size_arr()-1] <> rightTicks[get_size_arr()-1] ):
        if( leftTicks[get_size_arr()-1] > rightTicks[get_size_arr()-1] ):
            diff = ( leftTicks[get_size_arr()-1] - rightTicks[get_size_arr()-1] )
            global relativeAngle
            relativeAngle -= (diff * ticksMultiplier * .25)
        elif( rightTicks[get_size_arr()-1] > leftTicks[get_size_arr()-1] ):
            diff = ( rightTicks[get_size_arr()-1] - leftTicks[get_size_arr()-1] )
            global relativeAngle
            relativeAngle += (diff * ticksMultiplier * .25)
    if (relativeAngle > 360):
        relativeAngle = (relativeAngle - 360)
    if (relativeAngle < 0):
        relativeAngle = (relativeAngle + 360)
    return relativeAngle

def updateAngleLeft():
    global rotation
    left = leftTicks[get_size_arr()-2] - leftTicks[get_size_arr()-1]
    right = rightTicks[get_size_arr()-1]
    diff = right - left
    rotation += (diff * ticksMultiplier)
    if (rotation > 360):
            rotation = (rotation - 360)
    if (rotation < 0):
            rotation = (rotation + 360)
    #("rotation anticlockwise zero point: ",rotation)
    return rotation

def updateAngleRight():
    global rotation
    left = leftTicks[get_size_arr()-1]
    right = rightTicks[get_size_arr()-2] - rightTicks[get_size_arr()-1]
    diff = left - right
        #global relativeAngle
    rotation -= (diff * ticksMultiplier)
    if (rotation > 360):
            rotation = (rotation - 360)
    if (rotation < 0):
            rotation = (rotation + 360)
    #print("rotation clockwise zero point: ",rotation)
    return rotation

def updateAngleRev():
    global rotation
    if ( leftTicks[get_size_arr()-1] <> rightTicks[get_size_arr()-1] ):
            if( leftTicks[get_size_arr()-1] > rightTicks[get_size_arr()-1] ):
                    diff = ( leftTicks[get_size_arr()-1] - rightTicks[get_size_arr()-1] )
                    global relativeAngle
            #arbitraty .5 right now. This might need to be removed
                    relativeAngle += (diff * ticksMultiplier *.25)
            elif( rightTicks[get_size_arr()-1] > leftTicks[get_size_arr()-1] ):
                    diff = ( rightTicks[get_size_arr()-1] - leftTicks[get_size_arr()-1] )
                    global relativeAngle
                    relativeAngle -= (diff * ticksMultiplier *.25)
    if (relativeAngle > 360):
            relativeAngle = (relativeAngle - 360)
    if (relativeAngle < 0):
            relativeAngle = (relativeAngle + 360)
    return relativeAngle

def getAngle():
    angle = updateRA()
    return angle

def getRightDistArr():
    return rightDist

def getLeftDistArr():
    return leftDist

def setZero():
    leftDist.append(0)
    rightDist.append(0)

def getLastDist():
    return leftDist[len(leftDist)-1]

def getTotalDist():
    global distIndex
    
    distreturn = 0
    while distIndex != len(leftDist)-1:
        distIndex +=1;
        distreturn += ((leftDist[distIndex] + rightDist[distIndex])/2)
    return distreturn*1.3

def updateRA():
    global relativeAngle
    global rotation
    #global lastfortesting
    #if(rotation != 0 or lastfortesting != relativeAngle):
        #print("relative angle {}, rotation {}".format(relativeAngle,rotation));    
    #lastfortesting = relativeAngle
    tmp = relativeAngle + rotation
    if (tmp > 360):
        tmp = tmp - 360
    if(tmp < 0):
        tmp = tmp + 360
    rotation = 0
    relativeAngle = tmp
    return relativeAngle

def getLastCall():
    return lastCall
