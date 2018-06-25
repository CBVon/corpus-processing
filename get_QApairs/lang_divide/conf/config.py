#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This script is used for log the config used in the task of language_task
# Author by yannnli, Mail: wangzehui@sogou-inc.com, date: 2016-12-05

import os

#work_path
_data_path = "demo_forcorpus/data" #集群
#_data_path = "./data" #本地

#keyboards is used to classify all languaged by their unicodes
BASIC_LATIN= "id mg ms rw sw zu en enin uzlat".split()
EXTENDED_LATIN = "af az bslat cs da de es et eu fi frfr ga gl ha hr hu ig is it jv lt lv nl no pl pt ro sk sl sq su sv tl tr vi yo kulat srlat".split()#ca frca ptbr eslat removed
LATIN_EXTEND_ADDITIONAL = "yo vi ig".split()
ALL_LATIN = BASIC_LATIN+EXTENDED_LATIN
CYRILLIC = "be bg kk ky mk mn ru srcy tg tt uk".split()
ARABIC = "ar fa ps sdar ug ur".split()
MARK_ARABIC = "ar sdar".split()
DEVANAGARI = "hi ne mr".split()
BENGALI= "as bn".split()
ARABIC_FORMB = "ar ug".split()

PT = "pt".split()
ES = "es".split()
FR = "frfr".split()
#PT = "pt ptbr".split()
#ES = "es eslat".split()
#FR = "frfr frca".split()

#singleton unicode and shorthand corresponded
SINGLETONS = [
	('Ethiopic','am'),
	('Ethiopic Supplement','am'),
	('Ethiopic Extended','am'),
	('Tibetan', 'bo'),
	('Greek', 'el'),
	('Greek and Coptic','el'),
	('Gujarati', 'gu'),
	('Hebrew', 'he'),
	('Armenian', 'hy'),
	('Georgian', 'ka'),
	('Khmer', 'km'),
	('Kannada', 'kn'),
	('Lao', 'lo'),
	('Malayalam', 'ml'),
	('Gurmukhi', 'pa'),
	('Burmese', 'my'),
	('Oriya', 'or'),
	('Gurmukhi','pagur'),
	('Sinhala', 'si'),
	('Tamil', 'ta'),
	('Telugu', 'te'),
	('Thai', 'th'),
	('Mongolian', 'mn-Mong'),
]

_single = ['am','bo','el','gu','he','hy','ka','km','kn','lo','ml','pa','my','or','pagur','si','ta','te','th','mn-Mong']
ALL_LANGS = ALL_LATIN + CYRILLIC + ARABIC + DEVANAGARI + BENGALI + _single

#paths is used to log all the files needed in the task
paths={
	'dict_path':os.path.join(_data_path,"dict"),
	'unique_dict_path':os.path.join(_data_path,'uniquedict'),
	'unicodes_path':os.path.join(_data_path,'unicodes.txt'),
	'letter_path':os.path.join(_data_path,'letter_collect'),
	'ngrams_count_path':os.path.join(_data_path,'ngrams/ngrams_count'),
	'ngrams_freq_path':os.path.join(_data_path,'ngrams/ngrams_freq'),
	'words_model_path':os.path.join(_data_path,'words')
}

#settings is used to log all the variants in the task
settings={
	'UNKNOWN':'UNKNOWN',
	'MODEL':'distance',
	'VERBOSE':False,
	'LOOSE':False,
	'DICT_FREQ_LOW' : 0.4,        #logged words dict threshold
	'UNIQUE_LOW' : True           #match unique words with low formats
}

#settings for load pattern
load_settings={
	'DICT_FREQ':10000,             #threshold for check whether lowfreq word
	'NEPALI_DICT_FREQ' : 1000,     #special for nepali
	'WORD_NUM':8000,             #ngram count for every language
	'LOWFREQ_LOAD' : False         #whether to load full dict
}

#settings for distance_model
distance_settings={
	'CYRI_MAX_TRI_GRAMS' : 500,
	'CYRI_MAX_BI_GRAMS' : 500,
	'MAX_TRI_GRAMS' : 500,
	'MAX_BI_GRAMS' : 500,
	'MAX_UNI_GRAMS' : 300
}

#settings for bayes model
bayes_settings={
	'WORD_UNIS_FREQ' : 0.8,
	'ALPHA_DEFAULT' : 0.5,
	'ALPHA_WIDTH' : 0.05,
	'BASE_FREQ' : 10000,
	'CONV_THRESHOLD' : 0.99999,
	'ITERATION_LIMIT' : 2000,
	'n_trail' : 7,
	'WORD_UNIS_FREQ' : 0.8,
	'OUTPUT_THRESHOLD' : 0.4
}

#settings for words_model
words_settings={
	'WORDS_THRESHOLD_HIGH' : 0.6,   #threshold to check whether one language can be picked out
	'WORDS_THRESHOLD_LOW' : 0.4, #threshold to check whether load languages at the end
	'ITER_COUNT' : 5, #iter count for loop of result check
	'LOOSE' : True, #covert both words loaded and text word to lower format
	'OUTPUT_COUNT' : 10, #define the num of langs output in langs statistic
	'WORDS_LOADED' : 1000, #define the num of words to load
	'WORDS_CHECK_LOW' : 500, #define the lowest words check num in  the task
	'WORDS_CHECK_HIGH' : 5000,#define the highest words check num in the task
}
