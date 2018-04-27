import sys
import re
#python filter_map.py pt2w_indict.verbchanged


reload(sys)
sys.setdefaultencoding("utf-8")

verb_file = open(sys.argv[1], "r")
verb_list = []
for line in verb_file:
    verb_list.append(line.split('\t')[0])

reg = re.compile(u"[,\.!\?;&#\+\-\*\\/]+")

for line in sys.stdin:
    linelist = line.strip().split('\t')
    if len(linelist) != 2:
        continue
    sent = linelist[0].strip()
    sf = linelist[1]

    sent = sent.decode("utf-8")
    sent = sent.lower()
    sent = sent.encode("utf-8")
    
    sub_sent = re.sub(reg, "", sent).strip()
    sent_list = sub_sent.split(' ')
    #print sent_list[1], len(sent_list[1])
    while "" in sent_list:
        sent_list.remove("")

    if len(sent_list) < 3:
        continue
    sent_list[0] = ""
    sent_list[1] = ""

    for verb in verb_list:
        if verb in sent_list:
            print sent + "\t" + sf
            break

