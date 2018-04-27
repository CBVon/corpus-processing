#coding: utf-8
import sys


in_file = open(sys.argv[1], "r")
in_list = in_file.readlines()
ind = 0
is_repeat = False

pair_set = set([]) #重复的pair不必重复输出

for i in xrange(len(in_list)):
    if in_list[i][0] == '#':
        if i + 1 < len(in_list) and in_list[i+1][0] != '#':
            if in_list[i] in pair_set:
                is_repeat = True
                continue
            is_repeat = False
            ind += 1
            print str(ind) + "\t" + in_list[i][1:],
            pair_set.add(in_list[i])
        continue

    if in_list[i][0] == "\n":
        continue
    
    if not is_repeat:
        print in_list[i],
