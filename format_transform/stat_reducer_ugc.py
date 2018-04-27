import sys


freq_s = 0
pre_lang = ""
pre_text = ""
for line in sys.stdin:
    line = line.strip()
    infos = line.split("\t")
    if len(infos) != 2:
        continue
    lang = infos[0].strip()
    text = infos[1].strip()
	
    if (pre_lang != "" and lang != pre_lang) or (pre_text != "" and text != pre_text):
        print pre_lang + "\t" + pre_text + "\t" + str(freq_s)
        pre_text = text
        pre_lang = lang
        freq_s = 1
        continue

    pre_text = text
    pre_lang = lang
    freq_s += 1
        
if freq_s > 0:
    print pre_lang + "\t" + pre_text + "\t" + str(freq_s)
