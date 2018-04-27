#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This script provides tageted funcs used in langugae_task
# Author yannnli, Mail wangzehui@sogou-inc.com

from conf.config import SINGLETONS,CYRILLIC,ARABIC,DEVANAGARI,LATIN_EXTEND_ADDITIONAL,EXTENDED_LATIN,ARABIC_FORMB,BENGALI,PT,ALL_LATIN
from conf.config import settings,bayes_settings
from distance_model import language_check_distance
from bayes_model import language_check_bayes,word_sequence_check
from words_model import language_check_words
from loadFunc import unique_words_map
from basicFunc import get_dicts_count,_word_unis,_letter_unis

UNKNOWN = settings['UNKNOWN']
detect_type = settings['MODEL']
verbose = settings['VERBOSE']

#this function is used to write back to interface the result of the project
#if matched to one single unis, the func can return the language directly
#else, forward check
def _detect(text,unis):
	if unis==[]:
		return UNKNOWN

	if "Hangul Syllables" in unis or "Hangul Jamo" in unis or "Hangul Compatibility Jamo" in unis or "Hangul" in unis:
		return "ko"

	if "Greek and Coptic" in unis:
		return "el"

	if "Katakana" in unis:
		return "ja"

	for uniName, langName in SINGLETONS:
		if uniName in unis:
			return langName

	if "CJK Unified Ideographs" in unis or "Bopomofo" in unis or "Bopomofo Extended" in unis or "KangXi Radicals" in unis:
		return "zh"

	if "Cyrillic" in unis:
		return lang_check( text, CYRILLIC,"CYRILLIC" )

	if "Arabic" in unis or "Arabic Presentation Forms-A" in unis or "Arabic Presentation Forms-B" in unis:
		if "Arabic Presentation Forms-B" in unis:
			return lang_check(text,ARABIC_FORMB,"ARABIC_FORMB")
		return lang_check( text, ARABIC,"ARABIC")

	if "Devanagari" in unis:
		return lang_check( text, DEVANAGARI,"DEVANAGARI")

	if "Latin Extended Additional" in unis:
		return lang_check( text,LATIN_EXTEND_ADDITIONAL,"LATIN_EXTEND_ADDITIONAL")

	if "Extended Latin" in unis:
		latinLang = lang_check( text, EXTENDED_LATIN,"EXTENDED_LATIN")
		if latinLang == "pt":
			return lang_check(text, PT,"PT")
		else:
			return latinLang
	
	if "Bengali" in unis:
		return lang_check(text, BENGALI, "BENGALI")
	
	if "Basic Latin" in unis:
		latinLang = lang_check(text, ALL_LATIN,"ALL_LATIN")
		if latinLang == "pt":
                        return lang_check(text, PT,"PT")
                else:
                        return latinLang

	return UNKNOWN

#this func aims at return unique language containing any word in a sequence
def unique_lang_get(text,uni_type):
	if settings['UNIQUE_LOW']:
		text = text.lower()
	text_items = text.split(' ')
	for text_item in text_items:
		if unique_words_map[uni_type].has_key(text_item):
			if verbose:
				print text.encode('utf-8')+" has unique word "+text_item.encode('utf-8')+" in dict "+unique_words_map[uni_type].get(text_item)
			return unique_words_map[uni_type].get(text_item)

#this func is used to identity the text to one languge in one uni_type
def lang_check(text, unis, uni_type):
	#First of all, if up detect_type is words,skip pre tasks
	if detect_type == 'words':
		return language_check_words(text,unis)
	'''#1. get logged words probability, if below dict_freq_low, continue
	dict_freq = get_dicts_count(text)
	if verbose:
		print text.encode('utf-8')+"'s dict_freq is "+str(dict_freq)
	if dict_freq < settings['DICT_FREQ_LOW']:
		return UNKNOWN
	#2. check whether the text has word belonging to the unique dict
	if unique_words_map.has_key(uni_type):
		lang_unique_detect = unique_lang_get(text,uni_type)
		#if lang_unique_detect!=None:
		#	return lang_unique_detect
	#3. combine letter_unis and sequence unis
	letter_unis = _letter_unis(text)
	if verbose:
		print text.encode('utf-8')+"'s letter unis is"
		print letter_unis
	unis = list(set(unis).intersection(set(letter_unis)))'''
	#4. get langcheck_result accoring to detect_type
	if detect_type=='bayes':
		seq_unis = _word_unis(text)
		original_freq = word_sequence_check(text,unis)
		if verbose:
			print text.encode('utf-8')+"'s original freq is"
			print original_freq
		if verbose:
			print text.encode('utf-8')+"'s word unis is"
			print seq_unis
		if len(seq_unis)==0:
			return original_freq
		word_unis_freq = word_sequence_check(text,seq_unis)
		total_dict = {}
		if isinstance(original_freq,list):
			for i in range(0,len(original_freq)):
				total_dict[original_freq[i][0]]=original_freq[i][1]*(1-bayes_settings['WORD_UNIS_FREQ'])
		if word_unis_freq==UNKNOWN and original_freq==UNKNOWN:
			return UNKNOWN
		for word_pair in word_unis_freq:
			word_lang = word_pair[0]
			word_freq = word_pair[1]
			if total_dict.has_key(word_lang):
				total_dict[word_lang]+=bayes_settings['WORD_UNIS_FREQ']*word_freq
			else:
				total_dict[word_lang] = bayes_settings['WORD_UNIS_FREQ']*word_freq
		if verbose:
			print text.encode('utf-8')+"'s new freq is"
			print word_unis_freq
		return sorted(total_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
	elif detect_type=='distance':
		lang_detected = language_check_distance(text,unis,uni_type,0)
		return lang_detected
