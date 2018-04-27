#! /usr/bin/env python
# -*- coding: utf8 -*-
import sys
import re
import os,codecs
import numpy as np
#from gensim.models import word2vec
#from gensim.models.word2vec import LineSentence
from sklearn.ensemble import RandomForestClassifier

reload(sys)
sys.setdefaultencoding('utf-8')

langtag = sys.argv[1]

#base_path='python_27/python27/resource'
#os.chdir(base_path)
#test = open('python_27/python27/include/python2.7/code.h','r')

input_negative = codecs.open('negtive_tw_train_rule_1000000.txt', 'r')
input_postive = open('postive_tw_train_rule_1000000.txt', 'r')
#model = word2vec.Word2Vec.load('word_embedding_1000000')

charlistFILE = str('Char.sort.txt')
charlistfile = open(charlistFILE, 'r')
uselesslistFILE = str('dict.freq.sort.lowerFreq.sort.txt')
uselesslistfile = open(uselesslistFILE, 'r')
charDic = {}
uselessDic = {}
checkDic = {}
ugc_checkDic = {}

for lines in charlistfile:
    lines = lines.strip()
    line_list = lines.split("\t")
    if len(line_list) == 2:
        charDic[line_list[1]] = line_list[0]

for lines in uselesslistfile:
    lines = lines.strip()
    uselessDic[lines.split("\t")[0]] = 1


#判断是否全为数字
def isnumeric(word):
    return all(c in "0123456789.+-%/,:()[]=#&" for c in word) 



# 单词首字母是大写的统计
def StaticUppercaseHeadLetter(line):
    line_list = line.split(' ')
    upper_num = 0
    lowwer_num = 0
    for line_word in line_list:
        if len(line_word) == 0:
            continue
        s = line_word[0]
        if charDic.has_key(s):
            upper_num += 1
        else:
            lowwer_num += 1
    return upper_num, lowwer_num, upper_num / (upper_num + lowwer_num)


# 所有单词都是大写的统计
def StaticUppercaseWord(line):
    line_list = line.split(' ')
    upper_num = 0
    lowwer_num = 0
    upper_length_list = {}
    upper_average_length = 0
    upper_sum_length = 0
    upper_max_length = 0
    upper_min_length = 0
    for line_word in line_list:
        flag = 0
        for i in range(len(line_word)):
            s = line_word[i]
            if charDic.has_key(s):
                continue
            else:
                flag = 1
        if flag == 0:
            upper_num += 1
            upper_length_list[line_word] = len(line_word)
            upper_sum_length += len(line_word)
            if len(line_word) > upper_max_length:
                upper_max_length = len(line_word)
            if len(line_word) < upper_min_length:
                upper_min_length = len(line_word)
        else:
            lowwer_num += 1
    if upper_num > 0:
        upper_average_length = upper_sum_length / upper_num
    upper_rate = upper_num / (upper_num + lowwer_num)

    return upper_num, lowwer_num, upper_rate, upper_length_list, upper_average_length, upper_max_length


# 判断特殊语句
def RemoveSpecialSentence(line):
    str_special = 'top social artist | automatically checked by | your profile | Twitter profile | vote for for | for the top |Check this out |' \
                  'social artist award | youTube video | youTube | FOLLOW ME | I posted a new | Click Here | Check it out | Check out |Just posted a photo |' \
                  ' More for | Top social artist | top social artist | Check it out| the top social| for the top| vote for for| social artist award| looking forward to|' \
                  ' I vote for| for top social| Check this out| Check out| for the follow| This is awesome| my vote for| want to see| to find out| voting for for| for for top|' \
                  ' to win a| a chance to | my twitter| My twitter| Find out| check out this| I am voting| am voting for| look forward to | Thanks for following| thanks for following|this is awesome |' \
                  ' to vote for| Check out my| find out who| chance to win| your twitter profile | your twitter profile| who visits your| entered to win| TODAY WE FIGHT| I\'m voting for|' \
                  ' can you follow| I just entered| Check out the| enters my Twitter |enjoy our daily|Enjoy our daily|#mPLUSRewards|for the full video|For the full video|get the full video| surely interest you |' \
                  'View the full video|View the Full|Get Android adult videos app|automatically checked by|youTube video|@YouTube|#youtube|#YouTube|youTube|FOLLOW ME|I posted a new|Click here|I\'m earning |' \
                  'Click Here|Just posted a|More for|Check out|check out|a chance to win|Do you want to|If you want to|new follower|Hello people in|I vote for|I\'ve just watched episode|check it out|check this out|' \
                  'Just the one new follower|Just the one unfollower|unfollower(.*?)follower|follower(.*?)unfollower|I gained \d follower|\d follower|\d unfollower|\d new follower|\d new unfollower |this is awesome |' \
                  'View our latest opening | Come hangout with me | Come give me a call | I literally | Top Social Artist Award | I\'m earning |On Social Media | Shout Out To My Ex | You have to see this |ask or confess |' \
                  'Ask or confess |Can you recommend |Interested in a #job |View our latest opening '

    for item in str_special.split('|'):
        remove_s1 = re.compile(item)
        if remove_s1.search(line):
            return '1\t1\t1\t1\t1'
    return '0\t0\t0\t0\t0'


# 统计单词长度
def StaticWordLwngth(line):
    line_list = line.split(' ')
    line_length = {}
    sum = 0
    for line_word in line_list:
        line_length[line_word] = len(line_word)
        sum += len(line_word)
    return sum / len(line_list), line_length


# 非常用词统计
def StaticUselessWord(line):
    line_list = line.split(' ')
    sum = 0
    for line_word in line_list:
        if uselessDic.has_key(line_word):
            sum += 1
    return sum, sum / len(line_list)


# 得到规则的特征
def getBasicRuleFeature(line_str):
    flagSpecialSentence = RemoveSpecialSentence(line_str)

    line_sentence = line_str
    upper_num, lowwer_num, upper_rate = StaticUppercaseHeadLetter(line_sentence)
    upper_num_1, lowwer_num_1, upper_rate_1, upper_length_list, upper_average_length_1, upper_max_length_1 = StaticUppercaseWord(line_sentence)
    average_lenth, length_list = StaticWordLwngth(line_sentence)
    uselessSum, uselessSumRate = StaticUselessWord(line_sentence)
    feature_str = str(flagSpecialSentence) + '\t' + str(upper_num) + '\t' + str(lowwer_num) + '\t' + str(
            upper_rate) + '\t' + str(upper_num_1) + '\t' + str(lowwer_num_1) + '\t' \
                      + str(upper_rate_1) + '\t' + str(upper_average_length_1) + '\t' + str(
            upper_max_length_1) + '\t' + str(average_lenth) + \
                      '\t' + str(uselessSum) + '\t' + str(uselessSumRate)
                      
    return feature_str



def read_data(data_file, data_set, tag, data_target):
    for line in data_file:
        line = line.strip()
        temp = []
        line_str = line.split('\t')
        for i in range(len(line_str)):
            temp.append(float(line_str[i]))
        if tag == 1:
            data_target.append(1)
        elif tag == 0:
            data_target.append(0)
        data_set.append(temp)


def get_predict_model(train, train_target):
    rfc = RandomForestClassifier(n_estimators=250).fit(np.array(train), np.array(train_target))
    return rfc


def get_predict_result(str_feature, rfc):
    test_sample = []
    temp = []
    line_str = str_feature.split('\t')
    for i in range(len(line_str)):
        temp.append(float(line_str[i]))
    test_sample.append(temp)
    y_pred = rfc.predict(np.array(test_sample))
    return y_pred[0]
#对评论语句进行ugc分类预测
def process():
    train = []
    train_target = []
    read_data(input_negative, train, 0, train_target)
    read_data(input_postive, train, 1, train_target)
    rfc = get_predict_model(train, train_target)
    
    for line in sys.stdin:
        try:
            line = line.strip()
	    infos = line.split('\t')
	    if len(infos) != 3:
	        continue

	    lang = infos[0].strip()
	    if lang != langtag:
	        continue
            sentence = infos[1].strip()
	    ori_sentence = sentence
	    sf = infos[2].strip()
            
	    sentence = re.sub('[^a-zA-Z]',' ',sentence).strip()
            if len(sentence)<2:
                continue
            line_list = sentence.split(' ')
            temp_list = []
            feature_simple_list = []
            temp_str = ''
            for i in range(len(line_list)):
                if len(line_list[i].strip())>1 and not isnumeric(line_list[i].strip()):
                    temp_str += line_list[i]+' '
            
            if len(temp_str)<1:
                continue
            str_feature_rule = getBasicRuleFeature(temp_str.strip())
            str_feature = str_feature_rule
            result = get_predict_result(str_feature, rfc)

            if result == 1:
                print lang + "\t" + sentence + "\t" + sf
        except Exception, ex:
            continue

process()

