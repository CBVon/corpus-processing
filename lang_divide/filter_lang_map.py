import sys


lang = sys.argv[1]

for line in sys.stdin:
    linelist = line.strip().split('\t')
    if len(linelist) != 3:
        continue
    thislang = linelist[0]
    if thislang == lang:
        print linelist[1] + "\t" + linelist[2]

