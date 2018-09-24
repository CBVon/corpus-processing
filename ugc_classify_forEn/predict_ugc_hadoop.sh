#!/bin/bash
source /etc/profile
source ~/.bash_profile

hadoopcmd=`which hadoop`
hadconf="/etc/hadoop1.0/conf"
hstream="/usr/local/hadoop1.0/contrib/streaming/hadoop-streaming-0.20.2-cdh3u4.jar"

datatype=$1
#inputpart=$2

lang=$2

#inputdir="/user/ime/tanglianrui/dl_corpus/$1/split_freq/part-*"
inputdir="/user/ime/fengchaobing/dl_corpus/${datatype}/get_QApairs/lang_divide/${lang}/part-*"
#outputdir="/user/ime/tanglianrui/dl_corpus/$1/ugc_classify/${lang}"
outputdir="/user/ime/fengchaobing/dl_corpus/${datatype}/get_QApairs/ugc_classify/${lang}/"

$hadoopcmd --config "$hadoopconf" fs -rmr ${outputdir};
$hadoopcmd --config "$hadoopconf" jar "$hstream" \
        -D mapred.job.name="ugc predict forEn" \
        -D stream.non.zero.exit.is.failure=false \
        -D mapred.map.tasks=10000 \
        -D mapred.reduce.tasks=0 \
        -archives hdfs://master01.zeus.hadoop.ctc.sogou-op.org:6230/user/ime/leiguocheng/tools/python_test.tar.gz#python_27 \
        -mapper "python_27/python27/bin/python ./rule_word2vec_feature_extract_new.py ${lang}"\
        -file rule_word2vec_feature_extract_new.py\
	    -file negtive_tw_train_rule_1000000.txt \
	    -file postive_tw_train_rule_1000000.txt\
	    -file Char.sort.txt\
	    -file dict.freq.sort.lowerFreq.sort.txt\
        -input ${inputdir} \
        -output ${outputdir}

