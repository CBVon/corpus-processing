#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This script is used to load all the files
# Author yannnli, Mail wangzehui@sogou-inc.com

import re,os,codecs
from conf.config import SINGLETONS,CYRILLIC,ARABIC,DEVANAGARI,LATIN_EXTEND_ADDITIONAL,EXTENDED_LATIN,ARABIC_FORMB,BENGALI,PT,ALL_LATIN,BASIC_LATIN,MARK_ARABIC,ALL_LANGS
from conf.config import paths
from conf.config import settings
from conf.config import load_settings
from conf.config import words_settings
from collections import defaultdict

detect_type = settings['MODEL']
verbose = settings['VERBOSE']

models={}
models['trigrams']={}
models['bigrams']={}
models['unigrams']={}

unique_words_map = {}
unique_words_map['BASIC_LATIN']={}
unique_words_map['EXTENDED_LATIN']={}
unique_words_map['CYRILLIC']={}
unique_words_map['ARABIC']={}
unique_words_map['DEVANAGARI']={}
unique_words_map['MARK_ARABIC']={}
unique_words_map['ALL_LATIN']={}

grammaps={}
lang_probs=defaultdict(float)

words_dict={}
lowfreq_dict={}
letters_dict={}

words_model=defaultdict(list)

#this func is a basic func but used in loadfunc,so located here
#this func is used to normalize a list of prob and return the max prob in it
def normalizeProb(prob):
	maxp = 0.0
	sump = 0.0
	for lang in prob.keys():
		sump += prob[lang]
	if sump == 0.0:
		return prob,maxp
	for lang in prob.keys():
		prob_val = prob.get(lang)
		prob_val /= sump
		if maxp < prob_val:
			maxp = prob_val
		prob[lang] = prob_val
	return prob,maxp

#This func is used to load all the unicodes
def load_unicodes():
	file = open(paths['unicodes_path'])
	line = file.readline()
	splitter = re.compile(r'^(....)\.\.(....); (.*)$')
	endloc_list = []
	uni_names_list = []
	for line in file:
		if line.startswith('#'):
			continue
		line = line.strip()
		if not line:
			continue
		unis = splitter.match(line)
		if unis is not None:
			end_loc = int(unis.group(2),16)
			name = unis.group(3)
			endloc_list.append(end_loc)
			uni_names_list.append(name)
	return endloc_list,uni_names_list

_endloc,_uni_names=load_unicodes()

#This func is used to load all unique files
def _load_unique_models():
	wordsDir = paths['unique_dict_path']
	wordslist = os.listdir(wordsDir)
	if verbose:
		print "unique words loaded begin..."
	for lang_file in wordslist:
		lang_file_path = os.path.join(wordsDir,lang_file)
		if os.path.getsize(lang_file_path)==0:
			continue
		input_types = []
		f = codecs.open(lang_file_path,'r','utf-8')
		if BASIC_LATIN.count(lang_file)>0:
			input_types = 'ALL_LATIN'.split()
		if EXTENDED_LATIN.count(lang_file)>0:
			input_types = 'EXTENDED_LATIN ALL_LATIN'.split()
		if CYRILLIC.count(lang_file)>0:
			input_types = 'CYRILLIC'.split()
		if ARABIC.count(lang_file)>0:
			input_types = 'ARABIC'.split()
		if DEVANAGARI.count(lang_file)>0:
			input_types = 'DEVANAGARI'.split()  
		if MARK_ARABIC.count(lang_file)>0:
			input_type = 'MARK_ARABIC ARABIC'.split()		
		if len(input_types) == 0:
			continue
		for line in f:
			if not line.strip():
				continue
			for input_type in input_types:
				if settings['UNIQUE_LOW']:
					unique_words_map[input_type][line.strip().lower()] = lang_file
				else:
					unique_words_map[input_type][line.strip()] = lang_file
		if verbose:
			print lang_file+" loaded..."

_load_unique_models()

#this func is used to load letters of all languages
#after loaded, the letter form is letters_dict[letter]=[lang1,lang2...lang_n]
def _load_letters():
	letterDir = paths['letter_path']
	letterlist = os.listdir(letterDir)
	if verbose:
		print "letters loaded begin..."
	for letter_file in letterlist:
		if ALL_LANGS.count(letter_file)==0:
			continue
		letter_file_path = os.path.join(letterDir,letter_file)
		if os.path.getsize(letter_file_path)==0:
			continue
		f = codecs.open(letter_file_path,'r','utf-8')
		for line in f:
			line = line.strip()
			line_items = line.split('\t')
			#if len(line_items)<2:
			#	continue
			letter = line_items[0].replace('\r','')
			if not letters_dict.has_key(letter):
				letters_dict[letter]=[]
			letters_dict[letter].append(letter_file)
	if verbose:
		print "letters loaded end"

_load_letters()

#this func is used to load words whose freq >$DICT_FREQ from file into words_dict
#after loaded, the dict form is words_dict[word]="[lang1,lang2....,lang_n]"
#AS the dict resource is not standard now, DICT_FREQ is changed for some special case
#prefix, dicsource file must be sorted reversely
def _load_words():
	dictDir = paths['dict_path']
	dictlist = os.listdir(dictDir)
	if verbose:
		print "words loaded begin..."
	for dict_file in dictlist:
		if ALL_LANGS.count(dict_file)==0:
			continue
		if verbose:
			print dict_file+" loaded"
		dict_file_path = os.path.join(dictDir,dict_file)
		if dict_file.startswith("."):
			continue
		if os.path.getsize(dict_file_path)==0:
			continue
		dict_freq = load_settings['DICT_FREQ']
		if dict_file == "ne":
			dict_freq = load_settings['NEPALI_DICT_FREQ']
		f = codecs.open(dict_file_path,'r','utf-8')
		for line in f:
			line = line.strip()
			line_items = line.split('\t')
			if len(line_items)<2:
				continue
			text = line_items[0]
			freq = int(line_items[1])
			if freq>dict_freq:
				if not words_dict.has_key(text):
					words_dict[text]=[]
				words_dict[text].append(dict_file)
			else:
				if not load_settings['LOWFREQ_LOAD']:
					break # for function test
				if not lowfreq_dict.has_key(text):
					lowfreq_dict[text]=[]
				lowfreq_dict[text].append(dict_file)
		
_load_words()

def _load_ngrams(init_type):
	#gramsDir = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'ngrams2')
	if init_type=="distance":
		gramsDir = paths['ngrams_count_path']
	else:
		gramsDir = paths['ngrams_freq_path']
	#gramslist = os.listdir(gramsDir)
	words_total_freq=0.0
	for gram_dir in ['unigrams','bigrams','trigrams']:
		modelsDir = os.path.join(gramsDir,gram_dir)
		if gram_dir=='trigrams':
			lineRe = re.compile(r"(.{3})\s+(.*)")
		elif gram_dir=='bigrams':
			lineRe = re.compile(r"(.{2})\s+(.*)")
		elif gram_dir == 'unigrams':
			lineRe = re.compile(r"(.{1})\s+(.*)")
		if verbose:
			print modelsDir
		modelsList = os.listdir(modelsDir)
		for modelFile in modelsList:
			modelPath = os.path.join(modelsDir, modelFile)
			if os.path.isdir(modelPath):
				continue
			f = codecs.open(modelPath, 'r', 'utf-8')
			model = {}  # QHash<QString,int> model
			words_freq = 0.0
			lang_name = modelFile.lower()
			word_count = 0
			for line in f:
				word_count += 1
				if word_count>load_settings['WORD_NUM']:
					break
				m = lineRe.search(line)
				if m:
					try:
						word_freq = int(m.group(2))
						model[m.group(1)] = word_freq
						words_freq += word_freq
					except Exception,e:
						print e
						print modelPath+' '+m.group(1)+' '
			if init_type=='distance':
				models[gram_dir][lang_name] = model
			elif init_type=='bayes':
				lang_probs[lang_name]+=words_freq
				for word in model.keys():
					if not grammaps.has_key(word):
						grammaps[word]={}
					grammaps[word][lang_name]=model[word]/words_freq
				words_total_freq+=words_freq
		for word in grammaps.keys():
			grammaps[word],max_waste = normalizeProb(grammaps[word])
		for key in lang_probs.keys():
			lang_probs[key] = lang_probs.get(key)/words_total_freq

#this function is used to load words_model data
def _load_wordsmodel():
	wordsDir = paths['words_model_path']
	langlist = os.listdir(wordsDir)
	for lang in langlist:
		words_lang_path = os.path.join(wordsDir,lang)
		if os.path.isdir(words_lang_path):
				continue
		words_lang_file = codecs.open(words_lang_path, 'r', 'utf-8')
		load_count = 0
		for line in words_lang_file:
			load_count += 1
			if load_count>words_settings['WORDS_LOADED']:
				break
			line = line.strip()
			if words_settings['LOOSE']:#if loose model, convert all langs to lower format
				line = line.lower()
			words_model[line].append(lang)

#this function is used to init models
def _load_models(detect_type):
	if detect_type=="bayes" or detect_type=="distance":
		_load_ngrams(detect_type)
	else:
		_load_wordsmodel()

_load_models(detect_type)
