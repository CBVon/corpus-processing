#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# This script provides interface for outside
# Author yannnli, Mail wangzehui@sogou-inc.com

import unicodedata,sys
from conf.config import settings
from language_detect import _detect
from basicFunc import _unis
from basicFunc import _normalize
UNKNOWN = settings['UNKNOWN']

#this function is used to output the language detect task
def language_detect(text):
	if not text:
		return UNKNOWN
	if isinstance(text,str):
		try:
			text=unicode(text,'utf-8')
			text = _normalize(text)
			return _detect(text,_unis(text))
		except Exception,e:
			sys.stderr.write("ERROR COVERT TEXT TO UTF-8 OR ERROR IN DETECTION == "+text+"\n")
			return UNKNOWN
