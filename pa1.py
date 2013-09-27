from itertools import groupby
from collections import defaultdict
import csv
reader = csv.reader(open('pa1.csv','rU'))
data = [ (int(row[0]),int(row[1]),float(row[2])) for row in reader ]

cntx = defaultdict(int)


sumv = 0
for k,g in groupby(data,lambda x:x[0]):
    sumv +=1
    for item in g:
        cntx[item[1]]+=1

def getxand(x):
    ret = defaultdict(int)
    for k,g in groupby(data,lambda x:x[0]):
        movies = map(lambda x:x[1],g)
        if x in movies:
            for item in movies:
                if item!=x:
                    ret[item]+=1
    return ret

req = [36955, 36658, 786]

def calc1(x,y,xand):
    return 1.0*xand[y]/cntx[x]

def calc2(x,y,xand):
    return 1.0*calc1(x,y,xand) / (cntx[y]-xand[y]) *(sumv - cntx[x])  

def calc(x,f):
    xand = getxand(x)
    lst = [ (y,f(x,y,xand)) for y in cntx.keys()]
    lst.sort(key=lambda x:x[1],reverse=True)
    return lst[:5]

def disp(req,f):
    for x in req:
        lst = [x]
        res = calc(x,f)
        for item in res:
            lst.append(item[0])
            lst.append('%.2lf' %(item[1]))
        print ','.join(map(str,lst))

disp(req,calc1)
disp(req,calc2)
    
