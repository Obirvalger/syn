import sys

nodeFile = open(sys.argv[1])
plFile = open(sys.argv[2])
netFile = open(sys.argv[3])
#~ plFile = open(sys.argv[2])

ObjectDB = {}
NetDB = {}

class vertex:
    def _Init__(self, x, y, terminal = None):
        self.x = int(x)
        self.y = int(y)
        self.terminal = terminal

for line in nodeFile:
    words = line.split()
    if (len(words) == 0 or words[0] == '#' or words[0] == 'UCLA'):
        pass
    elif (words[0] == 'NumNodes'):
        numObjFromFile = words[2]
    elif (words[0] == 'NumTerminals'):
        numTermFromFile = words[2]
    else:
        ObjectDB[words[0]] = vertex(*words[1:])

indexNet = 0
for line in netFile:
    words = line.strip().split()
    if (len(words) == 0 or words[0] == '#' or words[0] == 'UCLA'):
            pass
    elif (words[0] == "NumNets"):
        numNetFromFile = words[2]
    elif (words[0] == "NumPins"):
      numPinFromFile = words[2]

    ThisNumPin  = words[2]
    ThisNetName = words[3]

    NetDB[ThisNetName] = indexNet
    indexNet += 1
  
    thisNetWl = 0
    ThisNetLx = 100000000
    ThisNetLy = 100000000
    ThisNetHx = -1
    ThisNetHy = -1
  
    for (i = 0 i < thisNumPin i += 1):
            line = <NETFILE>
        line =~ s/^\s+// # removes front/end white spaces
        line =~ s/\s+//
        @words = split(/\s+/, line)

        objName = words[0]
        inOut   = words[1]
        xOffset = words[3]
        yOffset = words[4]

        if (!defined(ObjectDB{objName})):
            print "\tERROR: Object objName is NOT defined in ObjectDB.\n"
        myExit()

        objLx = {ObjectDB{objName}}[LOCXINDEX]
        objLy = {ObjectDB{objName}}[LOCYINDEX]
        objDx = {ObjectDB{objName}}[DXINDEX]
        objDy = {ObjectDB{objName}}[DYINDEX]

        objCx = objLx + (objDx/2)
        objCy = objLy + (objDy/2)

        objX = objCx + xOffset
        objY = objCy + yOffset

        if (objX < thisNetLx):
            thisNetLx = objX

        if (objY < thisNetLy):
            thisNetLy = objY

        if (objX > thisNetHx):
            thisNetHx = objX

        if (objY > thisNetHy):
            thisNetHy = objY

        numPin += 1

    
    thisNetWl = ((thisNetHx - thisNetLx) + (thisNetHy - thisNetLy))
    TotalWl += thisNetWl
    numNet += 1


