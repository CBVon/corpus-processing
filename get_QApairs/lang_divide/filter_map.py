#coding: utf-8
import sys
import glob
import re


from src.language_detect_interface import language_detect


reload(sys)
sys.setdefaultencoding('utf-8')


lang = sys.argv[1]

 
#this function output the first lang detected
def get_lang(lang_detect):
    if isinstance(lang_detect,str):
        return lang_detect
    elif isinstance(lang_detect,list):
        #in case of bayes or words output
        #1. case of bayes output of lang,prob
        if isinstance(lang_detect[0],tuple):
            lang_real = lang_detect[0][0]
        #2. in case of words output of list of langs
        elif isinstance(lang_detect[0],str):
            lang_real = lang_detect[0]
        return lang_real


def loadFilterChars():
    #files = glob.glob("./character/" + lang.capitalize() + ".txt") #本地
    files = glob.glob("demo_forcorpus/character/" + lang.capitalize() + ".txt") #集群 #这里只处理一个 语言
    chars = set()
    for fpath in files:
        f = open(fpath)
        for line in f.readlines():
            line = line.decode("utf-8")
            if line.strip() == "":
                continue
            ch = line.strip().split("\t")[0]
            if ch == "-":
                continue
            chars.add(ch)
    return u"[" + u"".join(chars) + u"]+"


filter_chars = loadFilterChars() #['&/.ACBEDGFIHKJMLONQPSRUTWVYXZ\acbedgfihkjmlonqpsrutwvyxz]+ 
filter_chars = re.sub(r"['&/.\\]", "", filter_chars) #去除标点（杂质）, 有则删除  # [ACBEDGFIHKJMLONQPSRUTWVYXZacbedgfihkjmlonqpsrutwvyxz]+
#print filter_chars
filter_pattern = re.compile(filter_chars + r"|[\-,\.:;!\?_ 0-9\'\"]+") # [ACBEDGFIHKJMLONQPSRUTWVYXZacbedgfihkjmlonqpsrutwvyxz]+|[-,;!?_ 0-9]+
#print filter_chars + u"|[-,;!?_ ]+|\s+|\d+"
#print filter_chars + u"|[-,;!?_ 0-9]+"

sys.stderr.write(filter_chars + r"|[\-,\.:;!\?_ 0-9]+")

def format(str):    
    str_list = re.findall(filter_pattern, str)
    str_list = [i for i in str_list if i != ""]
    str = u" ".join(str_list)
    
    str = str.lstrip('-,.;!? ')
    str = re.sub(r"(\\\.)+", "\.", str)
    str = re.sub('\s+', ' ', str) #多个空格 变1个
    str = re.sub(r'[,]+', ',', str) #多个 , 变1个
    str = re.sub(r'[\.]+', ',', str) #多个 . 变1个
    str = re.sub("(, )+", ", ", str)
    str = re.sub(r"(\. )+", "\. ", str)
    return str.strip()


for line in sys.stdin:
    
    linelist = line.strip().split('\t')
    if len(linelist) != 2:
        continue
    Q = linelist[0].strip()
    A = linelist[1].strip()
    
    if Q == "" or A == "":
        continue

    #print Q, A
    #print line.strip()

    lang_detect_Q = language_detect(Q)
    lang_real_Q = get_lang(lang_detect_Q)
    lang_detect_A = language_detect(A)
    lang_real_A = get_lang(lang_detect_A)

    if lang_real_Q != lang or lang_real_A != lang:
        continue

    Q = format(Q)
    A = format(A)
    """
    try:
        lang_detect_Q = language_detect(Q)
        lang_real_Q = get_lang(lang_detect_Q)
        lang_detect_A = language_detect(A)
        lang_real_A = get_lang(lang_detect_A)
    
        #print lang_real_Q, lang_real_A

        if lang_real_Q != lang or lang_real_A != lang:
            continue
    
        Q = format(Q)
        A = format(A)
    except Exception, err:
        sys.stderr.write("lang_detect Exception : " + line)
        sys.stderr.write(str(err) + "\n")
        continue
    """
    if Q != "" and A != "":
        print Q + "\t" + A







