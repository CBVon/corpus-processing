#coding: utf-8
#python remove_appro.py facebook_es_top_freq_1000.txt es_fb_ugc_part.txt 
#编辑因为很多条目重复的原因， 没有全部找出ugc。 本程序通过相似度来找到所有 ugc；反之为非ugc

import sys


def lcs_len(s1,s2):
    m=[[0 for i in range(len(s2)+1)]  for j in range(len(s1)+1)]
    mmax=0
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i]==s2[j]:
                m[i+1][j+1]=m[i][j]+1
                if m[i+1][j+1]>mmax:
                    mmax=m[i+1][j+1]
    return mmax


all_file = open(sys.argv[1], "r")
all_list = all_file.readlines()
all_list = [i.strip() for i in all_list]
part_file = open(sys.argv[2], "r")
part_list = part_file.readlines()
part_list = [i.strip() for i in part_list]


for line in all_list:
    is_print = False

    l = line.strip()
    if l in part_list:
        is_print = True

    alpha_num = 0
    for i in l:
        if i.isalpha():
            alpha_num += 1

    s = l.split('\t')[0]
    for line1 in part_list:
        s1 = line1.strip().split('\t')[0]
        if abs(len(s) - len(s1)) <= 10 and float(lcs_len(s, s1)) / min(len(s), len(s1)) > 0.5 and float(max(len(s), len(s1))) / min(len(s), len(s1)) < 2.0 and alpha_num > 1:
            is_print = True
            #print "line :  " + line
            #print "line1 : " + line1
            break
    
    #if is_print:#设置是否打印，进而输出到不同的 > output-file #python remove_appro.py facebook_es_top_freq_1000.txt es_fb_ugc_part.txt > es_fb_ugc.txt
    if not is_print: #python remove_appro.py facebook_es_top_freq_1000.txt es_fb_ugc_part.txt > es_fb_no_ugc.txt
        print line


