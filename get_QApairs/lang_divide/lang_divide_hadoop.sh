#!/bin/bash
#sh lang_divide_hadoop.sh facebook
source /etc/profile
source ~/.bash_profile

hadoopcmd=`which hadoop`
hadconf="/etc/hadoop1.0/conf"
hstream="/usr/local/hadoop1.0/contrib/streaming/hadoop-streaming-0.20.2-cdh3u4.jar"

datatype=$1
lang=$2

input="/user/ime/fengchaobing/dl_corpus/${datatype}/get_QApairs/origin_QApairs/part-*"
output="/user/ime/fengchaobing/dl_corpus/${datatype}/get_QApairs/lang_divide/${lang}"

$hadoopcmd --config "$hadoopconf" fs -rmr ${output}
$hadoopcmd --config "$hadoopconf" jar "$hstream" \
    -D mapred.job.name="get_QApairs - lang_divide, ${datatype}, ${lang}, fengchaobing" \
    -D mapred.job.priority="VERY_HIGH" \
    -D mapred.map.tasks=10000 \
    -D mapred.reduce.tasks=100 \
    -cacheArchive hdfs://master01.zeus.hadoop.ctc.sogou-op.org:6230/user/ime/wangzehui/tools/python27.tar.gz#py \
    -cacheArchive hdfs://master01.zeus.hadoop.ctc.sogou-op.org:6230/user/ime/wangzehui/get_QApairs/lang_divide/demo_forcorpus.tar.gz#demo_forcorpus \
    -input ${input} \
    -output ${output} \
    -mapper "py/python27/bin/python demo_forcorpus/filter_map.py ${lang}"\
    -reducer "cat"

