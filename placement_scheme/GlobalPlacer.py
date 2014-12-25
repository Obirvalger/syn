__author__ = 'elena'
import re
import numpy as np
from Tkinter import *
from PIL import Image
import Image, ImageDraw
import time


def read_data_from_file(filename):
    f = file(filename, 'r')
    data = f.read()
    f.close()
    return data


class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()

    def __exit__(self, type, value, traceback):
        print "Elapsed time: {:.3f} sec".format(time.time() - self._startTime)


class VLSIPlacer:

    def __init__(self, notes_fn, nets_fn, scl_fn, pl_fn):
        self.notes_file = notes_fn
        self.nets_file = nets_fn
        self.scl_file = scl_fn
        self.pl_file = pl_fn

        self.rows = None
        self.number_of_rows = None
        self.nodes = None
        self.initial_position = None
        self.data_pl = None

    def global_placement(self):
        print('Global placing...')
        data = read_data_from_file(self.scl_file)

        f = False
        rows = []
        cur_row = []
        number_of_rows = 0
        for l in data.splitlines():
            if l == '':
                continue
            if 'CoreRow' in l:
                f = True
                cur_row.append(l.split()[1])
                continue
            if 'NumRows' in l:
                number_of_rows = l.split()[2]
                continue
            if 'End' in l:
                rows.append(cur_row)
                cur_row = []
                f = False
                continue
            if 'SubrowOrigin' in l:
                cur_row.append(l.split()[2])
                cur_row.append(l.split()[5])
                continue
            if f == True:
                cur_row.append(l.split()[2])

        #print(number_of_rows)
        #print(rows)
        #print(len(rows))

        data = read_data_from_file(self.notes_file)

        f = False
        nodes = []
        for l in data.splitlines():
            if f == True and l != '':
                if 'terminal' in l:
                    nodes.append(re.split('\s+', l)[1:])
                else:
                    cur_l = re.split('\s+', l)[1:]
                    cur_l.append('noterminal')
                    nodes.append(cur_l)
            if 'NumTerminals' in l:
                f = True

        data = read_data_from_file(self.pl_file)
        data_pl = data

        initial_position = {}
        for l in data.splitlines()[3:]:
            if l=='':
                continue
            else:
                lst = l.split()
                initial_position[lst[0]] = (int(float(lst[1])), int(float(lst[2])))

        d_nodes = {}
        i = 0
        for n in nodes:
            d_nodes[n[0]] = i
            i += 1

        ##c_matrix = np.zeros([len(nodes), len(nodes)])
        data = read_data_from_file(self.nets_file)

        f = False
        curNet = False
        cur_net = []
        nets = []
        for l in data.splitlines():
            if 'NetDegree' in l:
                curNet = True
                nets.append(cur_net)
                cur_net = []
                continue
            if f == True and l != '' and curNet == True:
                cur_net.append(re.split('\s+', l)[1])
            if 'NumPins' in l:
                f = True
        nets.append(cur_net)
        nets = nets[1:]
        '''
        for net in nets:
            for i in range(0, len(net)-1):
                for j in range(i+1, len(net)):
                    name1 = net[i]
                    name2 = net[j]
                    index1 = d_nodes[name1]
                    index2 = d_nodes[name2]
                    c_matrix[index1][index2] -= 1
                    c_matrix[index2][index1] -= 1
            for n in net:
                index = d_nodes[n]
                c_matrix[index][index] += 1

        print('Det(c_matrix)')
        print(np.linalg.det(c_matrix))
        print('Solving...')
        b = np.zeros(len(nodes))
        x = list(np.linalg.solve(c_matrix, b))
        y = list(np.linalg.solve(c_matrix, b))
        print(x)
        print(y)
        '''
        self.rows = rows
        self.number_of_rows = number_of_rows
        self.nodes = nodes
        self.initial_position = initial_position
        self.data_pl = data_pl


    def legalization(self):
        print('Legalization...')
        sites_per_row = self.rows[0][8]
        rows_height = self.rows[0][2]
        init_rows_position = map(lambda x: x[1], self.rows)
        #print(sites_per_row, rows_height, self.number_of_rows)
        #print(init_rows_position)
        number_of_rows = int(float(self.number_of_rows))

        #sites_matrix = np.zeros([number_of_rows, len(sites_per_row)])
        cells_positions = {}
        cur_row = 0
        cur_site = 0
        for n in self.nodes:
            if n[3] == 'terminal':
                cells_positions[n[0]] = self.initial_position[n[0]]
                continue
            if float(n[2]) != float(rows_height):
                print('Incorrect height of cell')
                break

            if cur_site + int(float(n[1])) <= int(float(sites_per_row)):
                #sites_matrix[cur_row][cur_site:cur_site+int(float(n[1]))] = 1
                cells_positions[n[0]] = (cur_site, int(float(init_rows_position[cur_row])))
                cur_site += int(float(n[1]))
            elif cur_row < number_of_rows - 1:
                cur_row += 1
                cur_site = 0
                cells_positions[n[0]] = (cur_site, int(float(init_rows_position[cur_row])))
                cur_site += int(float(n[1]))
            else:
                print('Error, not enough rows')
                break

        #print(cells_positions)
        new_pl = self.data_pl.splitlines()[:3]
        for n in self.nodes:
            new_pl.append(str(n[0]) + ' ' + str(cells_positions[n[0]][0]) + ' ' + str(cells_positions[n[0]][1]) + ' : N')
        #print(new_pl)
        #print('\n'.join(new_pl))
        new_data_pl = '\n'.join(new_pl)
        f = file('new.pl', 'w')
        f.write(new_data_pl)
        f.close()

        height = int(float(init_rows_position[len(init_rows_position) - 1]))+200
        width = int(float(sites_per_row))+200
        canvas = Canvas(height=height,width=width,bg='#222222')
        canvas.grid(row=0,column=1,rowspan=10)
        canvas.pack()
        for n in self.nodes:
            position = cells_positions[n[0]]
            c_width = int(float(n[1]))
            c_height = int(float(n[2]))
            canvas.create_rectangle(position[0]+50,position[1]+50,position[0]+c_width+50,position[1]+c_height+50, fill="blue")

        print('Saving images...')
        retval = canvas.postscript(file="placement.ps", height=height,
                                   width=width, colormode="color")
        inFile = Image.open("placement.ps")
        outFile = "placement.jpg"
        inFile.save(outFile)


def main():
    with Profiler() as p:
        #~ placer = VLSIPlacer('ibm01/ibm01.nodes', 'ibm01/ibm01.nets', 'ibm01/ibm01.scl', 'ibm01/ibm01.pl')
        #~ placer = VLSIPlacer('adaptec1/adaptec1.nodes', 'adaptec1/adaptec1.nets', 'adaptec1/adaptec1.scl', 'adaptec1/adaptec1.pl')
        placer = VLSIPlacer('adaptec2/adaptec2.nodes', 'adaptec2/adaptec2.nets', 'adaptec2/adaptec2.scl', 'adaptec2/adaptec2.pl')
        #~ placer = VLSIPlacer('adaptec3/adaptec3.nodes', 'adaptec3/adaptec3.nets', 'adaptec3/adaptec3.scl', 'adaptec3/adaptec3.pl')
        #~ placer = VLSIPlacer('bigblue1/bigblue1.nodes', 'bigblue1/bigblue1.nets', 'bigblue1/bigblue1.scl', 'bigblue1/bigblue1.pl')
        placer.global_placement()
        placer.legalization()

main()
