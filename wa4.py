import csv
from math import sqrt

with open('wa4.csv', 'rU') as csvfile:
    reader = csv.reader(csvfile)
    data = [row for row in reader]

    def process_cell(cell):
        cellsp = cell.split(':')
        if cellsp[0] == '':
            return 0
        else:
            return float(cellsp[0])

    def mymean(x):
        cnt = 0
        for k in x:
            cnt += (k != 0)
        return 1.0*sum(x)/cnt

    def sim(v1, v2):
        mv1 = mymean(v1)
        mv2 = mymean(v2)
        upper = 0.0
        lower1 = 0.0
        lower2 = 0.0
        for i in range(len(v1)):
            if v1[i] != 0 and v2[i] != 0:
                upper += (v1[i] - mv1)*(v2[i] - mv2)
            if v1[i] != 0:
                lower1 += (v1[i] - mv1)**2
            if v2[i] != 0:
                lower2 += (v2[i] - mv2)**2
        return upper/sqrt(lower1)/sqrt(lower2)

    data = [map(process_cell, row) for row in data]
    uids = map(int, data[0])[1:]
    mids = [int(row[0]) for row in data[1:]]
    ratings = [row[1:] for row in data[1:]]
    rvec = zip(*ratings)
    urdict = {uids[i]: rvec[i] for i in range(len(uids))}

    print sim(urdict[1648], urdict[5136])





