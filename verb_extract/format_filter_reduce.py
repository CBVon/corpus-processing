#coding: utf-8
#根据每个verb抽取最先出现的Top30 line
#在line首，添加#verb 
#python format_filter_reduce.py pt2w_indict.verbchanged
import sys
import re


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


verb_file = open(sys.argv[1], "r")
verb_dict = {}
verb_set = set([])
for line in verb_file:
    verb = line.strip().split('\t')[0]
    verb_dict[verb] = []
    verb_set.add(verb)

ind = 0
reg = re.compile(u"[,\.!\?;&#\+\-\*\\/]+")

for line in sys.stdin:
    ind += 1
    if ind % 100000 == 0:
        sys.stderr.write(str(ind) + "\n")
    
    linelist = line.strip().split('\t')
    if len(linelist) != 2:
        continue

    sent = linelist[0].strip()
    sf = linelist[1]
    
    origin_list = sent.split(' ') #原始串 的list
    sub_sent = re.sub(reg, "", sent).strip()
    sent_list = sub_sent.split(' ') #sub后 的list
    while "" in sent_list:
        sent_list.remove("")

    sent_list[0] = ""
    sent_list[1] = ""

    for word in sent_list:
        if word in verb_dict and word in origin_list: #同时确保， 当前word 在原始串是一个 “确切”的词

            is_remove = False
            #相似度去重
            for s in verb_dict[word]:
                s_list = s.strip().split(' ')
                ll = lcs_len(origin_list, s_list)
                appro = float(ll) / min(len(origin_list), len(s_list))
                if appro > 0.6 or (appro > 0.4 and abs(len(origin_list) - len(s_list)) <= 2 and min(len(origin_list), len(s_list)) > 8): #您的个人资料在过去2小时内已被6人查看#追求s之间的差异化
                    is_remove = True
                    break
            if is_remove:
                continue

            #add #verb0 #verb1...
            print_set = set([]) #控制 每个verb 只打印一次
            for word1 in origin_list:
                if word1 in verb_set and (word1 not in print_set): 
                    print "#" + word1,
                    print_set.add(word1)

            print "\t" + sent + "\t" +sf

            verb_dict[word].append(sent)
            if len(verb_dict[word]) == 30:
                verb_dict.pop(word)
                sys.stderr.write("pop: " + word + ", len(verb_dict) : " + str(len(verb_dict)) + "\n")
            break

