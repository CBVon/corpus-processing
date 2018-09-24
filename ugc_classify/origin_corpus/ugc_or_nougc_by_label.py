#python ugc_or_nougc_by_label.py facebook ru
import sys
import codecs

reload(sys) 
sys.setdefaultencoding('utf-8') 

datatype = sys.argv[1]
lang = sys.argv[2]

short_d = ""
if datatype == "facebook":
    short_d = "fb"
elif datatype == "instagram":
    short_d = "ins"
elif datatype == "twitter":
    short_d = "twt"
elif datatype == "vk":
    short_d = "vk"

#full_f = open(datatype + "_" + lang + "_top_freq_1000.txt", "r")
#full_f = open(lang + "_" + short_d + "_2000.txt")
#full_f = open(lang + "_" + short_d + "_2000_marked.txt")

top_l = open(lang + "/" + lang + "_" + short_d + "_tmp/" + datatype + "_" + lang + "_top_freq_1000.txt", "r").readlines()
random_l = open(lang + "/" + lang + "_" + short_d + "_tmp/" + lang + "_" + short_d  + "_1000lines.txt", "r").readlines()
all_l = top_l + random_l

ugc_f = open(lang + "/" + lang + "_" + short_d + "_ugc.txt", "w")
no_ugc_f = open(lang + "/" + lang + "_" + short_d + "_no_ugc.txt", "w")

#for line in full_f:
for line in all_l:

    line_l = line.strip().split('\t')

#    if len(line_l) == 2:
#        ugc_f.write(line_l[0] + "\t" + line_l[1] + "\n")
    if len(line_l) == 3:
        if line_l[2] == "1":
            ugc_f.write(line_l[0] + "\t" + line_l[1] + "\n")
        elif line_l[2] == "0":
            no_ugc_f.write(line_l[0] + "\t" + line_l[1] + "\n")


