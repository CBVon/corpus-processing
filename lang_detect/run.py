#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# this file is used to run all the scripts, used to detect languages and handle all kinds of inputs and outputs
# Author yannnli, Mail wangzehui@sogou-inc.com, Date: 2016-12-05

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

#this function outputs all the langs detected
def get_langs(lang_detect):
	if isinstance(lang_detect,str):
		return lang_detect
	elif isinstance(lang_detect,list) and isinstance(lang_detect[0],tuple):#in case of bayes model
		lang_real = lang_detect[0][0]+"("+str(lang_detect[0][1])+")"
		for i in range(1,len(lang_detect)):
			lang_real += "|"+lang_detect[i][0]+"("+str(lang_detect[i][1])+")"
		return lang_real
	elif isinstance(lang_detect,list) and isinstance(lang_detect[0],str):#in case of words model
		lang_real ="|".join(lang_detect)
		return lang_real

#this function handles situations with text\tfreq input and simple mark output
def bi_in_simple_out():
#	r_file = open("test")
#	for line in r_file:
	for line in sys.stdin:
		line = line.strip()
		line_items = line.split("\t")
		if len(line_items)!=2:
			sys.stderr.write("INPUT LINE ERROR FORMAT\n")
			sys.stderr.write("INPUT FORMAT IS TEXT[tab]FREQ\n")
			sys.stderr.write("INPUT LINE IS " + line + "\n")
			continue
		text =  line_items[0]
		freq = line_items[1]
		lang_detect = language_detect(text)
		lang_real = get_lang(lang_detect)
		print(lang_real + "\t" + line)


#this function handles situations with lang\ttext input and mixed output
def bi_in_mixed_out():
	for line in sys.stdin:
		line = line.strip()
		line_items = line.split("\t")
		if len(line_items)!=2:
			sys.stderr.write("INPUT LENGTH BLOW 2\n")
			continue
		lang = line_items[0]
		text = line_items[1]
		lang_detect = language_detect(text)
		lang_real = get_langs(lang_detect)
		print(lang_real+"\t"+lang+"\t"+text)

#this function handles situations with text input and simple mark output
def uni_in_simple_out():
	for line in sys.stdin:
		lang_detect  = language_detect(line)
		lang_real = get_lang(lang_detect)
		print(lang_real + "\t" + line)

#this function handles situations with cmd input with format as text and simple output
def cmd_in_simple_out():
	while True:
		line = raw_input("Enter your input: ")
		line = line.strip()
		lang_detect = language_detect(line)
		lang_real = get_lang(lang_detect)
		print (lang_real + "\t" + line)

#this function handles situations with cmd input with format as text and mixed output
def cmd_in_mixed_out():
	while True:
		line = raw_input("Enter your input: ")
		line = line.strip()
		lang_detect = language_detect(line)
		lang_real = get_langs(lang_detect)
		print (lang_real + "\t" + line)

#this function handles situations with uni input with format as text and mixed output
def uni_in_mixed_out():
	f = open('test1')
	for line in f:
	#for line in sys.stdin:
		line = line.strip()
		lang_detect  = language_detect(line)
		lang_real = get_langs(lang_detect)
		print(lang_real + "\t" + line)

#Init function
if __name__ == '__main__':
	cmd_in_simple_out()
	#cmd_in_mixed_out()
	#uni_in_simple_out()
	#uni_in_mixed_out()
	#bi_in_simple_out()
	#bi_in_mixed_out()
