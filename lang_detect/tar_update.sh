#!/usr/bin/bash

rm ./demo_forcorpus.tar.gz
#tar zcvf demo_forcorpus.tar.gz ./*
tar zcvf demo_forcorpus.tar.gz ./* --exclude=./lang_bk
hadoop fs -rmr /user/ime/wangzehui/language_detect/demo_forcorpus.tar.gz
hadoop fs -put ./demo_forcorpus.tar.gz /user/ime/wangzehui/language_detect/demo_forcorpus.tar.gz
