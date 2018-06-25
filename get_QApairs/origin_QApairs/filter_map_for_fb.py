#coding: utf-8
import sys
import json
import re


reload(sys)
sys.setdefaultencoding("utf-8")


pattern = re.compile(r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?|"
"[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+|"
"[a-zA-z]+://[^\s]*|"
"(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}|")
# Email地址/ 域名/ InternetURL/ 手机号码

pattern1 = re.compile(r"\d+\.\d+\.\d+\.\d+|"
"#[^\s]*|"
"@[^\s]*")
# IP地址/ #标签/ @艾特 # 拆分出来， 避免子集pattern干扰


def format(str):
    # remove "<br>"
    str = str.replace("<br>", "")
    
    # remove patern&1
    str = re.sub(pattern, "", str)
    str = re.sub(pattern1, "", str)
    
    """
    str = re.sub('\s+', ' ', str) #多个空格 变1个
    str = re.sub(r'[,]+', ',', str) #多个 , 变1个
    """

    return str


for line in sys.stdin:
    #sys.stderr.write(line)
    
    d_line = {}

    try:
        d_line = json.loads(line.decode("utf-8").strip())
    except Exception, err:
        sys.stderr.write(line)
        sys.stderr.write(str(err) + "\n")
        continue

    if "data" in d_line:
        for message_d in d_line["data"]:
            if "message" in message_d and "comments" in message_d:
                Q = message_d["message"].replace("\n", ". ").replace("\t", " ").encode("utf-8").strip()
                if Q != "" and "data" in message_d["comments"]:
                    for comment_d in message_d["comments"]["data"]:
                        if "message" in comment_d:
                            A = comment_d["message"].replace("\n", ". ").replace("\t", " ").encode("utf-8").strip()
                            if A != "":
                                
                                Q = format(Q)
                                A = format(A)
                                
                                if Q != "" and A != "":
                                    print Q + "\t" + A




    

