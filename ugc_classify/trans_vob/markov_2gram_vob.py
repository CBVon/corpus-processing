#coding: utf-8
#用来获取，非ugc的，二维-词转移-概率表。基于马尔科夫和2-gram进行实现
#注意b-启示概率； 这里不考虑终止概率，因为.和不同单词结尾概率差别太大，但是.结尾并没有实际意义


import sys
import cPickle


vob_dict = {"bbbegin":{}}

#file = open("es_fb_no_ugc.txt", "r")
file = open(sys.argv[1], "r") #python markov_2gram_vob.py ../origin_corpus/es_fb_no_ugc.txt es_fb_no_ugc_trans_vob.pkl
for line in file:
    #print line,
    line_list = line.strip().split('\t')
    if len(line_list) != 2:
        continue
    s = line_list[0]
    f = int(line_list[1].strip())

    #print s, f,
    s_list = s.split(' ')
    pre_word = "no_word"
    for word in s_list:
        break_flag = False
        maxl = 0
        pre_c = None
        for c in word:
            if pre_c == c:
                maxl += 1
                if maxl > 3:
                    break_flag = True
                    break
            else:
                maxl = 1
            pre_c = c

        if break_flag:
            break

        if len(word) == 0:
            continue
        if not vob_dict.has_key(word):
            vob_dict[word] = {}
        if pre_word != "no_word":
            if vob_dict[pre_word].has_key(word):
                vob_dict[pre_word][word] += f
            else:
                vob_dict[pre_word][word] = f
        elif pre_word == "no_word":
            if vob_dict["bbbegin"].has_key(word):
                vob_dict["bbbegin"][word] += f
            else:
                vob_dict["bbbegin"][word] = f
        pre_word = word

for i in vob_dict:
    vob_dict[i]["ooothers"] = 1

for i in vob_dict:
    sum_f = 0
    for j in vob_dict[i]:
        sum_f += vob_dict[i][j]
    for j in vob_dict[i]:
        vob_dict[i][j] = float(vob_dict[i][j]) / sum_f

#print vob_dict
cPickle.dump(vob_dict, open(sys.argv[2], "w"))
#cPickle.load(open("sys.argv[2]", "r"))








