#!/bin/bash
#sh ugc_classify_hadoop.sh facebook es
source /etc/profile
source ~/.bash_profile

#sh tar_update.sh

hadoopcmd=`which hadoop`
hadconf="/etc/hadoop1.0/conf"
hstream="/usr/local/hadoop1.0/contrib/streaming/hadoop-streaming-0.20.2-cdh3u4.jar"

datatype=$1
lang=$2

input="/user/ime/fengchaobing/dl_corpus/${datatype}/lang_divide/${lang}/part-*"
output="/user/ime/fengchaobing/dl_corpus/${datatype}/ugc_classify/${lang}/"

$hadoopcmd --config "$hadoopconf" fs -rmr ${output}
$hadoopcmd --config "$hadoopconf" jar "$hstream" \
    -D mapred.job.name="ugc_classify, ${datatype}, ${lang}, fengchaobing" \
    -D mapred.job.priority="HIGH" \
    -D mapred.map.tasks=10000 \
    -D mapred.reduce.tasks=1 \
    -D stream.num.map.output.key.fields=2 \
    -D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator   \
    -D mapred.text.key.comparator.options="-k2,2nr -k1,1" \
    -cacheArchive hdfs://master01.zeus.hadoop.ctc.sogou-op.org:6230/user/ime/leiguocheng/tools/python_test.tar.gz#python_27 \
    -cacheArchive hdfs://master01.zeus.hadoop.ctc.sogou-op.org:6230/user/ime/fengchaobing/targz/ugc_classify.tar.gz#ugc_classify \
    -input ${input} \
    -output ${output} \
    -mapper "python_27/python27/bin/python ugc_classify/filter_map.py ${lang} ${datatype}"\
    -reducer "cat"

