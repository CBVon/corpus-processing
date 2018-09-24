#coding: utf-8

import sys


lang = sys.argv[1]
datatype = sys.argv[2]
short_d = ""
if datatype == "facebook":
    short_d = "fb"
elif datatype == "instagram":
    short_d = "ins"
elif datatype == "twitter":
    short_d = "twt"

top1000_lines = [i.strip().split('\t')[0] for i in open(lang + "/" + lang + "_" +  datatype + "_top1000", "rb").readlines()]
ugc_lines = [i.strip().split('\t')[0] for i in open("../origin_corpus/" + lang  + "/" + lang + "_" + short_d + "_ugc.txt", "rb").readlines()]
#print top1000_lines[0]
#print ugc_lines[0]

right_line = 0
for i in top1000_lines:
    if i in ugc_lines:
        right_line += 1

print lang + " - " + datatype + " - acc : " + str(float(right_line) / len(top1000_lines)) 
