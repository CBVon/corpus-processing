#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This script is used to handle corpus task.
# Input, corpus line by line; Output, line\tlang_detected.
# Author yannnli, CBVon. Mail wangzehui@sogou-inc.com

import sys
from src.language_detect_interface import language_detect

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

if __name__=="__main__":
    langdict = dict()
    """
    langdict["es"] = set(["esLAT", "esUS", "es"])
    langdict["pt"] = set(["pt", "ptBR"])
    langdict["ru"] = set(["ru"])
    langdict["id"] = set(["id"])
    langdict["frfr"] = set(["frFR", "frCA", "fr"])
    #langdict["en"] = set(["en"])
    langdict["de"] = set(["de"])
    
    langdict["it"] = set(["it"])
    langdict["tl"] = set(["tl"])
    """
    #只针对 vk 
    langdict["ru"] = set(["ru"])
    
    
    
    #langdict["de"] = set(["de"]) # 20180530 de-debug

    for line in sys.stdin:
        line = line.strip()
        line_items = line.split('\t')
        if len(line_items) != 3:
            continue
        lang = line_items[0]
        text = line_items[1]
        sentence_freq = line_items[2]
        
        lang_detect = language_detect(text)
        lang_real = get_lang(lang_detect)
        #print "lang real : " + lang_real
        if lang_real not in langdict:
            continue
        else:
            if lang == "unk":
                if lang_real == "frfr":
                    print "fr\t" + text + "\t" + sentence_freq
                else:
                    print lang_real + "\t" + text + "\t" + sentence_freq
            elif lang in langdict[lang_real]:
                print lang + "\t" + text + "\t" + sentence_freq
