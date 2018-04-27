#coding: utf-8
#文件做差
#pred_facebook_es_top_freq_1000_iter1_20180408.txt pred_facebook_es_top_freq_1000_iter1_20180408_ugc.txt

#all_file = open("pred_facebook_es_top_freq_1000_iter1_20180408.txt", "r")
#sub_file = open("pred_facebook_es_top_freq_1000_iter1_20180408_ugc.txt", "r")

#python sub_file.py > es_ins_no_ugc.txt
all_file = open("instagram_es_top_freq_1000.txt", "r")
sub_file = open("es_ins_ugc.txt", "r")

#python sub_file.py  > es_twt_no_ugc.txt
all_file = open("twitter_es_top_freq_1000.txt", "r")
sub_file = open("es_twt_ugc.txt", "r")

all_lines = [i.strip() for i in all_file.readlines()]
sub_lines = [i.strip() for i in sub_file.readlines()]

for line in all_lines:
    if line in sub_lines:
        continue
    print line

"""
#新负：pred_facebook_es_top_freq_1000_iter1_20180408_no_ugc.txt + es_fb_no_ugc_iter1.txt - pred_facebook_es_top_freq_1000_iter1_20180408_ugc.txt

f1 = open("pred_facebook_es_top_freq_1000_iter1_20180408_no_ugc.txt", "r")
f2 = open("es_fb_no_ugc_iter1.txt", "r")
f3 = open("pred_facebook_es_top_freq_1000_iter1_20180408_ugc.txt", "r")

l1 = [i.strip() for i in f1.readlines()]
l2 = [i.strip() for i in f2.readlines()]
l3 = [i.strip() for i in f3.readlines()]

for line in l2:
    if line not in l1:
        l1.append(line)

for line in l3:
    if line in l1:
        l1.remove(line)

for line in l1:
    print line
""" 

#直接用 编辑器 处理也很不错
