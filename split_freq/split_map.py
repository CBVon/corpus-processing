#coding=utf-8
import sys,re


def get_sentence_clone(line):
	sentence_list = []
	line = line.strip()
	line = re.sub('"|”|“|', '', line)
	line = re.sub('\.', ' .\n', line)
	line = re.sub('\?', ' ?\n', line)
	line = re.sub('\!', ' !\n', line)
	line_list_one = line.split('\n')
	for item in line_list_one:
		#if re.search('\w+',item):
		sentence_list.append(item.strip())
	return sentence_list


for line in sys.stdin:
	info = line.strip().split('\t')
	if len(info) != 3:
		continue
	lang = info[0]
	text = info[1]
	sf = info[2]

	sentences = get_sentence_clone(text)
	for sent in sentences:
		print lang + "\t" + sent + "\t" + sf 

