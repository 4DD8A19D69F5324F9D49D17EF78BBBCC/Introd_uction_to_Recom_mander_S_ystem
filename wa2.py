import csv
with open('wa2.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    data = [ row[1:] for row in reader]
    def process_cell(cell):
        cellsp = cell.split(':')
        if cellsp[0]=='':
            return 0
        else:
            return int(cellsp[0])
    data = [ map(process_cell,row)  for row in data]
    ids = data[0]
    ratings = data[1:]


    def top5id(x):
        tmp=sorted(zip(ids,x),key=lambda x:x[1],reverse=True)
        tmp=tmp[:5]
        tmp=map(lambda x:x[0],tmp)
        return tmp
    def printline(x):
        for item in x:
            print item
    rt = zip(*ratings)
    mean = map( lambda x:sum(x)*1.0/len(filter(lambda x:x!=0,x)) ,rt)
    fourplus = map(lambda x:1.0*len(filter(lambda x:x>=4,x))/len(filter(lambda x:x!=0,x)),rt)
    ratingcount = map(lambda x:len(filter(lambda x:x!=0,x)) ,rt)
    startop = [0] * len(ids)
    for row in ratings:
        if row[0]!=0:
            for i in range(1,len(ids)):
                if row[i]!=0:
                    startop[i]+=1
    printline(top5id(mean))
    print
    printline(top5id(fourplus))
    print
    printline(top5id(ratingcount))
    print
    printline(top5id(startop))
    print
