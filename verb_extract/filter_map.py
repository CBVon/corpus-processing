#coding: utf-8
import sys
import re
#python filter_map.py pt2w_indict.verbchanged


reload(sys)
sys.setdefaultencoding("utf-8")

lang = sys.argv[1][: 2]
print lang

verb_file = open(sys.argv[1], "r")
verb_list = []
for line in verb_file:
    verb_list.append(line.strip().split('\t')[0])

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
    
    if lang == "ru":
        #if len(sent_list) < 4: #20180508: 调整长度限制
        #if len(sent_list) < 5: #20180509: ru的限制 再改成 句长>4
        if len(sent_list) < 7: #20180625: ru的限制 再改成 句长>6
            continue
    else:
        if len(sent_list) < 3:
            continue

    sent_list[0] = ""
    sent_list[1] = ""

    #20180509: 对于ru, 动词最起码在第五个位置 因为俄语表达比较随意
    #20180625: 针对ru，让前6悬空，也就是动词最起码出现在第七个位置
    if lang == "ru":
        sent_list[2] = ""
        sent_list[3] = ""
        sent_list[4] = ""
        sent_list[5] = ""

    for verb in verb_list:
        if verb in sent_list:
            print sent + "\t" + sf
            break

