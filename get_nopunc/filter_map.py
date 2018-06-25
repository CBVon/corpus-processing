import sys


for line in sys.stdin:
    linelist = line.strip().split('\t')
    if len(linelist) != 2:
        continue
    sent = linelist[0]
    sf = linelist[1]
    
    if len(sent) > 100 and (',' not in sent):
        print sent + "\t" + sf

