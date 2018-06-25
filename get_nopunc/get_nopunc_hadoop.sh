#!/bin/bash
#sh get_nopunc_hadoop.sh dbg_st en
source /etc/profile
source ~/.bash_profile

hadoopcmd=`which hadoop`
hadconf="/etc/hadoop1.0/conf"
hstream="/usr/local/hadoop1.0/contrib/streaming/hadoop-streaming-0.20.2-cdh3u4.jar"

datatype=$1
lang=$2

input="/user/ime/fengchaobing/dl_corpus/${datatype}/lang_divide/${lang}/part*"
output="/user/ime/fengchaobing/dl_corpus/${datatype}/get_nopunc/${lang}/"

$hadoopcmd --config "$hadoopconf" fs -rmr ${output}
$hadoopcmd --config "$hadoopconf" jar "$hstream" \
    -D mapred.job.name="get_nopunc, ${datatype}, ${lang}, fengchaobing" \
    -D mapred.job.priority="VERY_HIGH" \
    -D mapred.map.tasks=500 \
    -D mapred.reduce.tasks=1 \
    -D stream.num.map.output.key.fields=2 \
    -D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator   \
    -D mapred.text.key.comparator.options="-k2,2nr -k1,1" \
    -file filter_map.py \
    -input ${input} \
    -output ${output} \
    -mapper "python filter_map.py"\
    -reducer "cat"

