#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This script is used for words model
# Author yannnli, Mail wangzehui@sogou-inc.com

import sys
from loadFunc import words_model
from collections import defaultdict
from conf.config import words_settings,settings
from loadFunc import unique_words_map#as up detect is for latins, just use all_latin in this area

verbose = settings['VERBOSE']
UNKNOWN = settings['UNKNOWN']

langs_count = defaultdict(int)

#this function aims to check whether should to output result
def check_output(iter_count,text,is_last):
	if len(langs_count)==0:
		return UNKNOWN
	langs_sorted = sorted(langs_count.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
	max_value = langs_sorted[0][1]
	max_langs = []
	for (lang,lang_val) in langs_sorted:
		if lang_val < max_value:
			break
		max_langs.append(lang)
	#check return lang, if max_value meets some criteria,return max_lang
	if len(max_langs)==1 and max_value/float(iter_count) > words_settings["WORDS_THRESHOLD_HIGH"]:
		if verbose:
			sys.stdout.write("It's time to output the result of words model of text "+text.encode("utf-8")+"\n")
			for (lang_t,value_t) in sorted(langs_count.items(), lambda x, y: cmp(x[1], y[1]), reverse=True):
				sys.stdout.write("("+lang_t+","+str(value_t)+")\n")
		return max_langs
	else:
		if is_last:
			value_low = float(iter_count) * words_settings["WORDS_THRESHOLD_LOW"]
			for (lang,lang_val) in langs_sorted:
				if lang_val > value_low and lang_val < max_value:
					max_langs.append(lang)
			if len(max_langs)>0:
				return max_langs
			else:
				return UNKNOWN
		else:
			return UNKNOWN	

#this function aims to return the result of languge_check_words
def language_check_words(line,unis):
	text_items = line.split(" ")
	iter_count = 0
	langs_count.clear()
	for text in text_items:
		if words_settings['LOOSE']:#if loose model, change detected words to lower format
			text = text.lower()
		if words_model.has_key(text):
			text_langs = words_model.get(text)
			for lang in text_langs:
				langs_count[lang] += 1
			iter_count += 1
		else:
			continue
		#check if iter_count > check high threshold, if break
		if iter_count > words_settings["WORDS_CHECK_HIGH"]:
			break
		#check if meets ends threshold
		if iter_count>words_settings["WORDS_CHECK_LOW"] and iter_count%words_settings["ITER_COUNT"]==4:
			max_lang = check_output(iter_count,line,False)
			if max_lang != UNKNOWN:
				sys.stdout.write("iter_count === "+str(iter_count)+"\n")
				return max_lang
	max_lang = check_output(iter_count,line,True)
	sys.stdout.write("iter_count === "+str(iter_count)+"\n")
	return max_lang

#this function aims to return the language_login time map, for example language x appear in word index 1,3,4. iter_map[x]=[1,3,4]
def wordsmodel_dict_check(line):
	text_items = line.split(" ")
	words_count = 0
	#score all the data
	iter_map = defaultdict(list)
	#used to select output langs
	count_map = defaultdict(int)
	#used to select output unique langs
	unique_count_map = defaultdict(int)
	#the map to output
	return_map = defaultdict(list)
	#the unique_map
	unique_map = unique_words_map['ALL_LATIN']
	for text in text_items:
		words_count += 1
		if words_settings['LOOSE']:
			text = text.lower()
		if words_model.has_key(text):
			text_langs = words_model.get(text)
			return_map['total'].append(words_count)
			for text_lang in text_langs:
				iter_map[text_lang].append(words_count)
				count_map[text_lang] += 1
		if unique_map.has_key(text):
			unique_lang = unique_map.get(text)
			unique_count_map[unique_lang+"_unique"]+=1
			iter_map[unique_lang+"_unique"].append(words_count)
	return_map['total_count'] = words_count
	langs_sorted = sorted(count_map.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
	for i in range(0,min(len(langs_sorted),words_settings["OUTPUT_COUNT"])):
		(lang,count_list) = langs_sorted[i]
		return_map[lang] = iter_map[lang]
	unique_sorted = sorted(unique_count_map.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
	for i in range(0,min(len(unique_sorted),words_settings["OUTPUT_COUNT"])):
		(lang,count_list) = unique_sorted[i]
		return_map[lang] = iter_map[lang]
	return return_map
