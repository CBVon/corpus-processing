import sys
import re


reload(sys)
sys.setdefaultencoding("utf-8")

reg = re.compile(u"[.!?;&#]+")

for i in sys.stdin:
    line = i.strip()
    line_list = line.split('\t')
    if len(line_list) != 2:
        continue
    sent = line_list[0]
    sf = line_list[1]
    
    sent = sent.strip()
    sub_sent = re.sub(reg, "", sent).strip()
    if len(sub_sent.split(' ')) <= 2:
        continue

    sent = sent.decode("utf-8")
    sent = sent.lower()
    sent = sent.encode("utf-8")
    print sent + "\t" + sf
    
