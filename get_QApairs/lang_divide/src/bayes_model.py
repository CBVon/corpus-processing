#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This script is used for bayes model
# Author yannnli, Mail wangzehui@sogou-inc.com

import random
from collections import defaultdict
from basicFunc import get_dicts_count,_letter_unis,createOrderedWordModel
from loadFunc import normalizeProb,lang_probs,grammaps
from conf.config import bayes_settings
from conf.config import settings

verbose = settings['VERBOSE']
UNKNOWN = settings['UNKNOWN']

#This func is the whole bayes model
def language_check_bayes():
	#1. check the probability of the login word in the sentence
	dict_freq = get_dicts_count(text)
	if dict_freq < bayes_settings['DICT_FREQ_LOW']:
		return UNKNOWN	
	#2. letter unis get and combineds with the former unis
	letter_unis = _letter_unis(text)
	if verbose:
		print text.encode('utf-8')+"'s letter unis is"
		print letter_unis
		print text.encode('utf-8')+"'s word unis is"
		print seq_unis
		print
	unis = list(set(unis).intersection(set(letter_unis)))
	#3. original result get
	original_freq = word_sequence_check(text,unis)
	if verbose:
		print text.encode('utf-8')+"'s original freq is"
		print original_freq
	#4. sequence unis get
	seq_unis = _word_unis(text)
	if len(seq_unis)==0:
		return original_freq
	#5. mix sequence result and original result
	total_dict = {}
	word_unis_freq = word_sequence_check(text,seq_unis)
	if isinstance(original_freq,list):
		for i in range(0,len(original_freq)):
			total_dict[original_freq[i][0]]=original_freq[i][1]*(1-bayes_settings['WORD_UNIS_FREQ'])
	if word_unis_freq==UNKNOWN and original_freq==UNKNOWN:
		return UNKNOWN
	for word_pair in word_unis_freq:
		word_lang = word_pair[0]
		word_freq = word_pair[1]
		if total_dict.has_key(word_lang):
			total_dict[word_lang]+=WORD_UNIS_FREQ*word_freq
		else:
			total_dict[word_lang] = WORD_UNIS_FREQ*word_freq
	if verbose:
		print text.encode('utf-8')+"'s new freq is"
		print word_unis_freq
	return sorted(total_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)

#This func is used to go through all the text items and return
def word_sequence_check(text,unis):
	#1. get the ngram model from the text
	alpha = bayes_settings["ALPHA_DEFAULT"]
	model =  createOrderedWordModel(text)
	if verbose:
		print text.encode('utf-8') + "'s model ngrams are:"
		for model_r in model:
			print model_r.encode('utf-8'),
	#2. init the language prob
	langprob = defaultdict(float)
	for lang_name in unis:
		langprob[lang_name]=0.0
	uni_count = 0
	for uni in unis:
		if lang_probs.has_key(uni):
			uni_count += 1
	for uni in unis:
		if lang_probs.has_key(uni):
		#	langprob[uni] = 1.0/float(uni_count) /average pooling
			langprob[uni] = lang_probs.get(uni)
	langprob,max_prob_t = normalizeProb(langprob)
	if verbose:
		print "inital prob is "
		print langprob
	#3. init the variants
	alpha = alpha + random.normalvariate(0,1)*bayes_settings['ALPHA_WIDTH']
	count = 0
	hit_count = 0
	last_champion = ''
	#4. calculate the prob
	for model_r in model:
		if not grammaps.has_key(model_r):
			continue
		if model_r == ' ':
			continue
		langprob = update_prob(langprob,model_r,alpha)
		count += 1
		if count % 5 == 1:
			langprob,maxprob = normalizeProb(langprob)
			if maxprob > bayes_settings['CONV_THRESHOLD'] or count >= ['ITERATION_LIMIT']:
				if count >= bayes_settings['ITERATION_LIMIT']:
					break
				for lang_pos in langprob.keys():
					if langprob.get(lang_pos)==maxprob:
						champion = lang_pos
						break
				if champion == last_champion:
					hit_count += 1
					if hit_count == 2:
						break
				else:
					last_champion = champion
					hit_count = 0
	langprob,maxprob = normalizeProb(langprob)
	#5. output the result
	if maxprob<0.1:
		return UNKNOWN
	langs = sorted(langprob.keys(), key=lambda k: (-langprob[k], k))
	if verbose:
		print text.encode('utf-8') +"'s possible languages are: "
		for lang_pos in langs:
			if langprob.get(lang_pos)<0.1:
				break
			print lang_pos+"======"+str(langprob.get(lang_pos))
	max_prob = langprob.get(langs[0])
	return_list = {}
	for lang_pos in langs:
		lang_prob = langprob.get(lang_pos)
		if lang_prob/max_prob > bayes_settings['OUTPUT_THRESHOLD']:
			return_list[lang_pos] = lang_prob
	return_list = sorted(return_list.items(), lambda x, y: cmp(x[1], y[1]), reverse=True) 
	return return_list

#this func is used to random choose word from the word items, 
#until prob has been calculated certain times or the result comes up to some criteria
def word_check(text,unis):
	#1. get the word model from the text 
	alpha = bayes_settings["ALPHA"]
	model =  createOrderedWordModel(text)
	#2. init the lang probability
	langprob = defaultdict(float)
	for lang_name in unis:
		langprob[lang_name]=0.0
	#3. calculate the result
	for index in range(0,bayes_settings['n_trail']):
	#	prob_tmp = init_prob(unis)
		prob_tmp = {}
		uni_count = 0
		for uni in unis:
			if lang_probs.has_key(uni):
				uni_count += 1
		for uni in unis:
			if lang_probs.has_key(uni):
				prob_tmp[uni] = 1.0/float(uni_count)
		alpha = alpha + random.normalvariate(0,1)*bayes_settings['ALPHA_WIDTH']
		count = 0
		hit_count = 0
		last_champion = ''
		while True:
			r = random.randint(0,len(model)-1)
			if grammaps.has_key(model[r]):
				if model[r]==' ':
					continue
				prob_tmp = update_prob(prob_tmp,model[r],alpha)
				count = count + 1
				if count%5==1:
					prob_tmp,maxprob = normalizeProb(prob_tmp)
					if maxprob>bayes_settings['CONV_THRESHOLD'] or count >=bayes_settings['ITERATION_LIMIT']:
						if count >= bayes_settings['ITERATION_LIMIT']:
							break
						for lang_tmp in prob_tmp.keys():
							if prob_tmp.get(lang_tmp)==maxprob:
								champion = lang_tmp
								break
						if champion == last_champion:
							hit_count += 1
							if hit_count == 2:
								break
						else:
							last_champion = champion
							hit_count = 0
		for uni in langprob.keys():
			if not prob_tmp.has_key(uni):
				continue
			langprob[uni]+=prob_tmp[uni]/bayes_settings['n_trail']
	langprob,maxprob = normalizeProb(langprob)
	# output the result
	if max(langprob.values())<0.1:
		return UNKNOWN
	langs = sorted(langprob.keys(), key=lambda k: (-langprob[k], k))
	if verbose:
		print text.encode('utf-8') +"'s possible languages are: "
		for lang_pos in langs:
			if langprob.get(lang_pos)<0.1:
				break
			print lang_pos+"======"+str(langprob.get(lang_pos))
	return langs[0]

#this func is used to update the probability
def update_prob(prob,gram,alpha):
	weight = alpha/bayes_settings['BASE_FREQ']
	langprobmap = grammaps[gram]
	'''if verbose:
		print "gram "+gram.encode('utf-8')+"'s unis are:"
		count = 0
		langprob_sorted = sorted(langprobmap.iteritems(), key=lambda d:d[1], reverse = True)
		print langprob_sorted[0:5]'''
	for uni in prob.keys():
		if not langprobmap.has_key(uni):
			prob[uni]*=weight
			continue
		prob[uni]*=weight+langprobmap[uni]
	return prob

#this func is used to init the prob
def init_prob(unis):
	initprob = {}
	total_prob = 0.0
	for uni in unis:
		if not lang_probs.has_key(uni):
			continue
		initprob[uni]=lang_probs[uni]
		total_prob += initprob[uni]
	for uni in initprob.keys():
		initprob[uni] = initprob[uni]/total_prob
	return initprob
