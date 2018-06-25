#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This script provides basic text functions for text
# Author yannnli, Mail wangzehui@sogou-inc.com

import sys,re,unicodedata
from collections import defaultdict
from bisect import bisect_left
from conf.config import settings
from loadFunc import models,unique_words_map,grammaps,lang_probs,words_dict,lowfreq_dict,letters_dict,_endloc,_uni_names

loose = settings['LOOSE']
verbose = settings['VERBOSE']
spaceRe = re.compile('\s+', re.UNICODE)

#this func go through all the unicodes and return all the non_alpha
def _makeNonAlphaRe():
	nonAlpha = [u'[^']
	for i in range(sys.maxunicode):
		c = unichr(i)
		if c.isalpha(): nonAlpha.append(c)
	nonAlpha.append(u']')
	nonAlpha = u"".join(nonAlpha)
	return re.compile(nonAlpha)
	
nonAlphaRe = _makeNonAlphaRe()

#this func is used to convert text to normalized unicode
#Besides, it also can remove non-alpha chars and compress runs of spaces
def _normalize(text):
	text = unicodedata.normalize('NFC', text)
	text = nonAlphaRe.sub(' ', text)
	text = spaceRe.sub(' ', text)
	return text

#this func returns the unicode corresponding to a char
def _unicode_check(code):
	insert_index = bisect_left(_endloc,ord(code))
	#print insert_index
	if len(_endloc)==insert_index:
		print 'code out of index...'+code+'\n' #post_period change to logger 
		return 'NULL'''
	return _uni_names[insert_index]

#This func is used to return the possible unicodes for a sentence
def _unis(text):
	unis_list = defaultdict(int)
	total_count = 0
	for c in text:
		if c.isalpha():
			uni = _unicode_check(c)
			unis_list[uni]+=1
			total_count+=1
	relavant_uni = []
	for key,value in unis_list.items():
		perc = (value*100)/total_count;
		if perc>=40:
			relavant_uni.append(key)
		elif key == "Basic Latin" and (perc >= 15):
			relavant_uni.append(key)
		elif key == "Latin Extended Additional" and (perc >= 10):
			relavant_uni.append(key)
	if verbose:
		print text.encode('utf-8') +"'s relevant unis are: "
		print relavant_uni	
	return relavant_uni

#this func is used to go through the sentence one time and log the trigram
#besides, it deletes the *_* format
def createOrderedModel(text):
	tri_model = defaultdict(int)
	text = text.lower()
	tri_model[' '+text[0:2]]+=1
	for i in range(0,len(text)-2):
		tri_model[text[i:i+3]]+=1
	tri_model[text[len(text)-2:len(text)]+' ']+=1
	return_model = sorted(tri_model.keys(), key=lambda k: (-tri_model[k], k))
	for i in range(0,len(return_model))[::-1]:
                if len(return_model[i])==3:
                        if return_model[i][1]==' ':
                                del return_model[i]
	return return_model

#this func go through the sentence one time and return all the ngrams in the sentence
def createOrderedWordModel(word):
	wordgrams=[]
	word = word.lower()
	word_len = len(word)
	if word_len==0:
		return wordgrams
	wordgrams.append(word[0])
	wordgrams.append(' '+word[0])
	wordgrams.append(word[word_len-1]+' ')
	if word_len>1:
		wordgrams.append(' '+word[0:2])
		#wordgrams.append(word[word_len-2:word_len]+' ')
		wordgrams.append(word[0:2])
		if word_len >= 3:
			wordgrams.append(word[0:3])
			wordgrams.append(word[word_len-2:word_len])
			wordgrams.append(word[word_len-2])
			for i in range(1,len(word)-2):
				wordgrams.append(word[i:i+3])
				wordgrams.append(word[i])
				wordgrams.append(word[i:i+2])
		wordgrams.append(word[word_len-1])
	return wordgrams

#this function aims to return the num of dicts that contain words in the sequence
#pre: the sequence must not be none
def get_dicts_count(text):
	text = text.lower()
	# the latter six lines is for public test
	#if isinstance(text,str):
	#	try:
	#		text = unicode(text,'utf-8')
	#	except Exception,e:
	#		print text
	#text = normalize(text)
	#end
	text_items = text.split(" ")
	dict_count = 0.0
	for text_item in text_items:
		if words_dict.has_key(text_item) or lowfreq_dict.has_key(text_item):
			dict_count += 1
	return float(dict_count)/len(text_items)

#this func is used to check word by language and return langs that contain words in the sequence
#argv loose is used to restrict the range of the possible languages, if loose means v else means ^set
def _word_unis(text):
	text = text.lower()
	return_list = []
	text_items = text.split(' ')
	if len(text_items)==0:
		return return_list
	if loose:
		for text in text_items:
			text = text.strip()
			if words_dict.has_key(text):
				if verbose:
					print text.encode('utf-8')+" is in worddict:"
					for lang_p in words_dict.get(text):
						print lang_p,
					print
				if len(words_dict.get(text))==1:
					return words_dict.get(text)#if unique return
				for lang_p in words_dict.get(text):
					if return_list.count(lang_p)==0:
						if verbose:
							print lang_p + "added..."
						return_list.append(lang_p)
	else:
		if words_dict.has_key(text_items[0]):
			return_list = words_dict.get(text_items[0])
		for i in range(1,len(text_items)):
			text = text_items[i]
			if return_list == None:
				return_list = []
			if words_dict.has_key(text):
				if len(return_list)==0:
					break
				else:
					return_list=list(set(return_list).intersection(set(words_dict.get(text))))
	if return_list == None:
		return_list = []
        return return_list

#this func is used to check word by letter information
def _letter_unis(text):
	return_list = []
	is_flag = True
	for c in text:
		if c.isalpha():
			if return_list == None:
				return_list = []
			if not letters_dict.has_key(c):
				continue
			'''if verbose:
				print c.encode('utf-8')+" is in letterdict"
				print letters_dict.get(c)'''
			if len(return_list)==0:
				if is_flag:
					return_list = letters_dict.get(c)
				else:
					return return_list
			else:
				return_list = list(set(return_list).intersection(set(letters_dict.get(c))))
	if return_list == None:
		return_list = []
	return return_list
