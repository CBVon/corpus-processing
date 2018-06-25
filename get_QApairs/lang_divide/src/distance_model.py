#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This script is used for distance model
# Author yannnli, Mail wangzehui@sogou-inc.com

import re
from basicFunc import createOrderedModel
from conf.config import distance_settings
from conf.config import settings
from loadFunc import models

UNKNOWN = settings['UNKNOWN']
verbose = settings['VERBOSE']
spRe = re.compile(r"\s\s", re.UNICODE)

#This func is used to return the distance model result
def language_check_distance(text,unis,uni_type,max_type):
	if len(text)==1:
		return ngram_check(text,unis,1,uni_type,max_type)
	elif len(text)==2:
		return ngram_check(text,unis,2,uni_type,max_type)
	else:
		return ngram_check(text,unis,3,uni_type,max_type)

#calculate according to location in the ngram file
def _dist(model,model_loaded,MAXGRAMS):
	dist = 0
	for i, value in enumerate(model[:MAXGRAMS]):
		if not spRe.search(value):
			if not model_loaded.get(value):
				dist += MAXGRAMS
				continue
			if model_loaded.get(value)<MAXGRAMS:
				if verbose:
					print "("+value.encode('utf-8')+")\t"+str(model_loaded.get(value)),
				dist += abs(i - model_loaded[value])
			else:
				dist += MAXGRAMS
	if verbose:
		print
	return dist

#This func is used to calculate the distance result
#the max_type argv is used to tell the func the maxgrams's type, if 0, default; else as max_type transfers
def ngram_check(text,unis,gram_n,uni_type,max_type):
	known_models = {}
	#1. variants get
	if gram_n==3:
		model = createOrderedModel(text)
		known_models = models['trigrams']
		if max_type!=0:
			MAX_GRAMS = max_type
		elif uni_type == "CYRILLIC":
			MAX_GRAMS = distance_settings['CYRI_MAX_TRI_GRAMS']
		else:
			MAX_GRAMS = distance_settings['MAX_TRI_GRAMS']
	else:
		model = []
		model.append(text)
	if gram_n==2:
		known_models = models['bigrams']
		if uni_type == "CYRILLIC":
			MAX_GRAMS = distance_settings['CYRI_MAX_BI_GRAMS']
		else:
			MAX_GRAMS = distance_settings['MAX_BI_GRAMS']
	elif gram_n==1:
		known_models = models['unigrams']
		MAX_GRAMS = distance_settings['MAX_UNI_GRAMS']

	#2. calculate the result
	scores = []
	hit_scores={}
	for uni in unis:
		uni_l = uni.lower()
		if known_models.has_key(uni_l):
			if verbose:
				print uni_l
			scores.append((_dist(model,known_models[uni_l],MAX_GRAMS),uni))
	if not scores:
		return UNKNOWN
	if verbose:
		scores_sorted = sorted(scores,key=lambda score:score[0])
		print 'distance model result'
		for i in range(0,len(scores_sorted)):
			print scores_sorted[i],
		print
	return min(scores)[1]
