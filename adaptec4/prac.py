import sys

if (len(sys.argv) == 1):
    print 'Usage: progname file.aux'
    exit()
auxFile = open(sys.argv[1])
for x in auxFile.readline().split():
    if (x.find('.nodes') != -1):
        #~ print x
        nodeFile = open(x)
    if (x.find('.nets') != -1):
        #~ print x
        netFile = open(x)
    if (x.find('.pl') != -1):
        #~ print x
        plFile = open(x)
    if (x.find('.scl') != -1):
        #~ print x
        sclFile = open(x)
'''
nodeFile = open(sys.argv[1])
plFile = open(sys.argv[2])
netFile = open(sys.argv[3])
sclFile = open(sys.argv[4])
'''

objectDB = {}
netDB = {}
sclDB = []

class vertex:
    def __init__(self, x, y, terminal = False):
        self.xSize = int(x)
        self.ySize = int(y)
        self.terminal = bool(terminal)
    def plUpdate(self, x, y, orient, fixed = False):
        self.x = x
        self.y = y
        self.orientation = orient
        self.fixed = bool(fixed)

def parseNode(nodeFile):
    'generate lists with nodename xsize ysize [terminal]'
    for line in nodeFile:
        words = line.split()
        if (len(words) == 0 or words[0] == '#' or words[0] == 'UCLA'):
            pass
        elif (words[0] == 'NumNodes'):
            numObjFromFile = words[2]
        elif (words[0] == 'NumTerminals'):
            numTermFromFile = words[2]
        else:
            yield words

def parsePl(plFile):
    'generate lists with nodename x y direction [/Fixed]'
    for line in plFile:
        words = line.split()
        if (len(words) == 0 or words[0] == '#' or words[0] == 'UCLA'):
            pass
        else:
            try:
                del(words[words.index(':')])
            except ValueError:
                pass
            yield words

nodeParser = parseNode(nodeFile)
plParser = parsePl(plFile)
for x in nodeParser:
    objectDB[x[0]] = vertex(*x[1:])
for x in plParser:
    objectDB[x[0]].plUpdate(*x[1:])
'''
for line in nodeFile:
    words = line.split()
    if (len(words) == 0 or words[0] == '#' or words[0] == 'UCLA'):
        pass
    elif (words[0] == 'NumNodes'):
        numObjFromFile = words[2]
    elif (words[0] == 'NumTerminals'):
        numTermFromFile = words[2]
    else:
        objectDB[words[0]] = vertex(*words[1:])

for line in plFile:
    words = line.split()
    if (len(words) == 0 or words[0] == '#' or words[0] == 'UCLA'):
        pass
    else:
        try:
            del(words[words.index(':')])
        except ValueError:
            pass
        objectDB[words[0]].plUpdate(*words[1:])
'''

for line in sclFile:
    words = line.split()
    if (len(words) == 0 or words[0] == '#' or words[0] == 'UCLA'):
        pass
    elif (words[0] == 'NumRows'):
        numObjFromFile = words[2]
    else:
        if (words[0] == 'CoreRow'):
            l = []
            line = next(sclFile)
            while (line != 'End\n'):
                words = line.split()
                if (len(words) == 0 or words[0] == '#' or words[0] == 'UCLA'):
                    pass
                else:
                    l.append(words[2])
                    if (words[0] == 'SubrowOrigin'):
                        l.append(words[5])
                    line = next(sclFile)
            sclDB.append(list(l))

for line in netFile:
    words = line.split()
    if (len(words) == 0 or words[0] == '#' or words[0] == 'UCLA'):
            pass
    elif (words[0] == "NumNets"):
        numNetFromFile = words[2]
    elif (words[0] == "NumPins"):
      numPinFromFile = words[2]
    else:
        thisNumPin  = int(words[2])
        thisNetName = words[3]
        tmp = []
        for i in xrange(thisNumPin):
            line = next(netFile)
            words = line.split()
            try:
                del(words[words.index(':')])
            except ValueError:
                pass
            tmp.append(words)
        netDB[thisNetName] = list(tmp)

'''
aC = 0
for k, v in netDB.items():
    su = 0
    for x in v:
        if x[1] == 'O':
            su += 1
    if (su != 1):
        aC += 1
        
print aC
'''

#~ for x in sclDB:
    #~ print x

'''
nTerms, nCom, nFixed = 0, 0, 0
for key, value in objectDB.items():
    nCom += 1
    if value.terminal:
        nTerms += 1
    if value.fixed:
        nFixed += 1

print numTermFromFile, nTerms, numObjFromFile, nCom, nFixed
'''
