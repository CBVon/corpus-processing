#coding: utf-8
#process : id, pt
#python filer_map.py pairtxt_file pairtxt_line C_pair_a C_pair_b  
#注：这个map可以解决：词对词中包含多个词的情况。比如：very good

import sys


pair_file = open(sys.argv[1], "r")
pair_line = pair_file.readlines()[int(sys.argv[2])]
pair_line = pair_line.strip()
sys.stderr.write(pair_line)
#sys.stderr.write(sys.argv[3] + "\n")
pair_a = pair_line.split('\t')[int(sys.argv[3])]
pair_b = pair_line.split('\t')[int(sys.argv[4])]

a_list = pair_a.split(' ')
b_list = pair_b.split(' ')

sys.stderr.write(pair_a + "\n")
sys.stderr.write(pair_b + "\n")

for line in sys.stdin:
    #sys.stderr.write(str(len(line.split("\t"))) + "\n")
    #sys.stderr.write(line.split("\t")[2])
    sentence = line.split("\t")[0]
    freq = line.split('\t')[1]

    word_list = sentence.split(' ')
    if (not (a_list[0] in word_list and b_list[0] in word_list)) or pair_a == pair_b or len(word_list) > 100:
        continue
    
    min_dis = 10000
    a_ind = -1
    b_ind = -1

    i = 0
    while i < len(word_list):
        if a_list[0] != word_list[i] and b_list[0] != word_list[i]:
            i += 1
            continue

        is_a = False
        is_b = False
        if a_list[0] == word_list[i]:
            is_a = True
            for j in xrange(1, len(a_list)):
                if i + j >= len(word_list) or (i + j < len(word_list) and a_list[j] != word_list[i + j]):
                    is_a = False
                    break
        
        if b_list[0] == word_list[i]:
            is_b = True
            for j in xrange(1, len(b_list)):
                if i + j >= len(word_list) or (i + j < len(word_list) and b_list[j] != word_list[i + j]):
                    is_b = False
                    break

        if is_a and is_b:
            if len(pair_a) > len(pair_b):
                is_b = False
            else:
                is_a = False
        
        if is_a:
            a_ind = i
            if b_ind != -1:
                new_dis = abs(a_ind - b_ind)
                if new_dis < min_dis:
                    min_dis = new_dis
            a_ind += len(a_list) - 1
            i += len(a_list) - 1

        if is_b:
            b_ind = i
            if a_ind != -1:
                new_dis = abs(a_ind - b_ind)
                if new_dis < min_dis:
                    min_dis = new_dis
            b_ind += len(b_list) - 1
            i += len(b_list) - 1

        i += 1
    if min_dis > 3 and min_dis < 15:
        #print line.strip('\n') + str(min_dis)
        print line, 
