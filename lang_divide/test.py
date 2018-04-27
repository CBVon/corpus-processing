import sys


for i in sys.stdin:
    i0 = i.split('\t')[0]
    l0 = len(i0)

    i1 = i.split('\t')[1]
    l1 = len(i1)

    print i,
    print i0, i1, 
    print "End!"
    print l0, l1

