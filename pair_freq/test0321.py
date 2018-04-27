import sys


for i in sys.stdin:
    print i,
    ii = i.strip()
    l = i.split('\t')
    for word in l:
        print word, len(word)
