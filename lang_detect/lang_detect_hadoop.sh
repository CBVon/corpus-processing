#!/bin/bash
source /etc/profile
source ~/.bash_profile

hadoopcmd=`which hadoop`
hadconf="/etc/hadoop1.0/conf"
hstream="/usr/local/hadoop1.0/contrib/streaming/hadoop-streaming-0.20.2-cdh3u4.jar"

datatype=$1

input="/user/ime/fengchaobing/dl_corpus/$1/format_transform/part-*"
output="/user/ime/fengchaobing/dl_corpus/$1/lang_detect/"

#sh tar_update.sh

$hadoopcmd --config "$hadoopconf" fs -rmr ${output}
$hadoopcmd --config "$hadoopconf" jar "$hstream" \
    -D mapred.job.name="language detect, ${datatype}, fengchaobing" \
    -D mapred.job.priority="VERY_HIGH" \
    -D stream.num.map.output.key.fields=2 \
    -D mapred.text.key.partitioner.options="-k1,1" \
    -D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
    -D mapred.text.key.comparator.options="-k1,1 -k2,2" \
    -D mapred.map.tasks=500 \
    -D mapred.reduce.tasks=30 \
    -cacheArchive hdfs://master01.zeus.hadoop.ctc.sogou-op.org:6230/user/ime/wangzehui/tools/python27.tar.gz#py \
    -cacheArchive hdfs://master01.zeus.hadoop.ctc.sogou-op.org:6230/user/ime/wangzehui/language_detect/demo_forcorpus.tar.gz#demo_forcorpus \
    -mapper 'py/python27/bin/python demo_forcorpus/corpus_run.py' \
    -reducer "cat" \
    -input ${input} \
    -output ${output} \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner 

sh ../rm_hadoopDir_emptyFile.sh ${output} ${datatype}
