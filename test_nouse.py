import sys


file = open("vk_10000.txt", "r")

list = file.readlines()[:1000]

l = len(list)
for i in xrange(l):
    for j in xrange(l):
        ipid = list[i].split(' ')[0]
        jpid = list[j].split(' ')[0]
        if ipid == jpid:
            if list[i] == list[j]:
                continue
            print ipid, jpid
