#coding: utf-8
#统计pair-freq结果的，句长；
#便于估计合理的 filter 阈值，避免pair-freq出的评测集中句子过长（对于编辑，难以评估）
import sys


file = open(sys.argv[1], "r")
file_list = file.readlines()

sum_len = 0
sum_count = 0
sum_words_len = 0
for line in file_list:
    if line[0].isdigit():
        continue
    print "line : " + line
    print "ttttt : " + str(len(line.split('\t')))
    sent = line.split('\t')[0]
    #print sent, len(sent), len(sent.split(' '))
    sum_len += len(sent)
    sum_words_len += len(sent.split(' '))
    sum_count += 1

    
avg_len = float(sum_len) / sum_count
avg_words_len = float(sum_words_len) / sum_count

bigger_avg_count = 0
bigger_500_count = 0
bigger_1000_count = 0

bigger_avg_words_count = 0
bigger_50_words_count = 0
bigger_100_words_count = 0
for line in file_list:
    sent = line.split('\t')[0]
    if len(sent) > avg_len:
        bigger_avg_count += 1
    if len(sent) > 500:
        bigger_500_count += 1
    if len(sent) > 1000:
        bigger_1000_count += 1

    if len(sent.split(' ')) > avg_words_len:
        bigger_avg_words_count += 1
    if len(sent.split(' ')) > 50:
        bigger_50_words_count += 1
    if len(sent.split(' ')) > 100:
        bigger_100_words_count += 1

print "sum_count : " + str(sum_count)

print "----- -----"

print "sum_len : " + str(sum_len)
print "avg_len : " + str(avg_len)
print "bigger_avg_count : " + str(bigger_avg_count)
print "bigger_500_count : " + str(bigger_500_count)
print "bigger_1000_count : " + str(bigger_1000_count)

print "----- -----"

print "sum_words_len : " + str(sum_words_len)
print "avg_words_len : " + str(avg_words_len)
print "bigger_avg_words_count : " + str(bigger_avg_words_count)
print "bigger_50_words_count : " + str(bigger_50_words_count)
print "bigger_100_words_count : " + str(bigger_100_words_count)
