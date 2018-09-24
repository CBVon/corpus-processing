#!/bin/bash
source /etc/profile
source ~/.bash_profile

hadoopcmd=`which hadoop`
hadconf="/etc/hadoop1.0/conf"
hstream="/usr/local/hadoop1.0/contrib/streaming/hadoop-streaming-0.20.2-cdh3u4.jar"

datatype=$1

input="/user/ime/fengchaobing/dl_corpus/$1/lang_detect/part-*"
output="/user/ime/fengchaobing/dl_corpus/$1/split_freq/"

if [[ ${datatype} == "twitter" ]]
then
    input="/user/ime/fengchaobing/dl_corpus/$1/format_transform/part-*"
fi

$hadoopcmd --config "$hadoopconf" fs -rmr ${output}
$hadoopcmd --config "$hadoopconf" jar "$hstream" \
    -D mapred.job.name="split sentence and freq statistic, ${datatype}, fengchaobing" \
    -D mapred.job.priority="VERY_HIGH" \
    -D stream.num.map.output.key.fields=2 \
    -D mapred.text.key.partitioner.options="-k1,2" \
    -D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
    -D mapred.text.key.comparator.options="-k1,1 -k2,2" \
    -D mapred.map.tasks=10000 \
    -D mapred.reduce.tasks=100 \
    -input ${input} \
    -output ${output} \
    -file split_map.py \
    -file freq_reduce.py \
    -mapper "python split_map.py" \
    -reducer "python freq_reduce.py" \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner

#sh ../../rm_hadoopDir_emptyFile.sh ${outputdir}

