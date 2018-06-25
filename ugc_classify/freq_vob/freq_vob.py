#coding: utf-8
#通过 ugc和非ugc，来统计分别的词频；进而构建出各自词表；用于生成ugc的一个特征

#观测可得
#ugc词表较小；no_ugc词表较大。由于no_ugc普遍长很多
#ugc词表多语气词，俚语，情绪


import sys
import json

iatatype="facebook"
file = open(sys.argv[1], "r")
#python freq_vob.py ../origin_corpus/es_fb_ugc.txt > es_fb_ugc_vob.txt
#python freq_vob.py ../origin_corpus/es_fb_no_ugc.txt > es_fb_no_ugc_vob.txt
vob_dict = {}

for line in file:
    list = line.strip().split('\t')
    if len(list) != 2:
        continue
    s = list[0]
    f = int(list[1].strip())
    
    s_list = s.split(' ')
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
            continue

        if len(word) > 1:
            #print word, len(word)
            if vob_dict.has_key(word):
                vob_dict[word] += f
            else:
                vob_dict[word] = f

vob_list = sorted(vob_dict.items(),key = lambda x:x[1],reverse = True)

for i in vob_list:
    #print i
    #ui = json.dumps(i, encoding="utf-8", ensure_ascii=False)
    print i[0] + "\t" +  str(i[1])
