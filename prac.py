import sys
import numpy
from random import randint
from time import clock

beginTime = clock()

if (len(sys.argv) == 1):
    print 'Usage: progname file.aux'
    exit()
auxFile = open(sys.argv[1])
for x in auxFile.readline().split():
    if (x.find('.nodes') != -1):
        nodeFile = open(x)
    elif (x.find('.nets') != -1):
        netFile = open(x)
    elif (x.find('.pl') != -1):
        plFile = open(x)
    elif (x.find('.scl') != -1):
        sclFile = open(x)

nodeDB = {}
netDB = {}
sclDB = []

class vertex:
    def __init__(self, name, x, y, terminal = False):
        self.nets = []
        self.name = name
        self.xSize = x
        self.ySize = y
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
            words[1:3] = int(words[1]), int(words[2])
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
            words[1:3] = int(words[1]), int(words[2])
            yield words

def parseNet(netFile):
    'generate tuple with netname and list of lists with nodename I/O x y'
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
            tmp = set()
            for i in xrange(thisNumPin):
                line = next(netFile)
                words = line.split()
                try:
                    del(words[words.index(':')])
                except ValueError:
                    pass
                words[2:4] = float(words[2]), float(words[3])
                tmp.add(words[0])
            yield (thisNetName, set(tmp))

def parseScl(sclFile):
    'generate lists with Coordinate Height Sitewidth Sitespacing Siteorient Sitesymmetry SubrowOrigin NumSites'
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
                yield [int(i) for i in l]


netDB = numpy.array([x[1] for x in parseNet(netFile)])

for x in parseNode(nodeFile):
    nodeDB[x[0]] = vertex(*x)
for x in parsePl(plFile):
    nodeDB[x[0]].plUpdate(*x[1:])

print "Created nodeDB"

for x in netDB:
    for name in x:
        nodeDB[name].nets.append(x - {name})

print "Created netDB"

A, B = set(), set()

for x in nodeDB.values():
    t = randint(0,1)
    if t:
        A.add(x.name)
    else:
        B.add(x.name)
    x.pos = t

def area(A):
    s = 0
    for x in A:
        s += nodeDB[x].xSize * nodeDB[x].ySize

    return s
    
vmax = max([x.xSize for x in nodeDB.values() if not x.terminal])
Amin = area(A) + area(B) - vmax
Amax = Amin + 2 * vmax

g = {}

for name, val in nodeDB.items():
    FS, TE = 0, 0
    for net in val.nets:
        netpos = set([nodeDB[x].pos for x in net])
        if len(netpos) == 1:
            if netpos.pop() == val.pos:
                TE += 1
            else:
                FS += 1
    g[name] = FS - TE

print "Time: {}".format(clock() - beginTime)

#~ for x in parseNet(netFile):
    #~ netDB[x[0]] = x[1:]
#~ for x in parseScl(sclFile):
    #~ sclDB.append(x)
