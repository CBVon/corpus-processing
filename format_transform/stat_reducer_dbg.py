import sys


freq_s = 0
pre_lang = ""
pre_text = ""
for line in sys.stdin:
    line = line.strip()
    infos = line.split("\t")
    #print len(infos)
    if len(infos) != 3:
        continue
    lang = infos[0].strip()
    text = infos[1].strip()
    sf = int(infos[2])

    if (pre_lang != "" and lang != pre_lang) or (pre_text != "" and text != pre_text):
        print pre_lang + "\t" + pre_text + "\t" + str(freq_s)
        pre_lang = lang
        pre_text = text
        freq_s = sf
        continue

    pre_lang = lang
    pre_text = text
    freq_s += sf
        
if freq_s > 0:
    print  pre_lang + "\t" + pre_text + "\t" + str(freq_s) 
