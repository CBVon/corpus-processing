#!/bin/bash
source /etc/profile
source ~/.bash_profile

datatype=$1
reducerfile=""

if [[ ${datatype} == "facebook" || ${datatype} == "instagram" || ${datatype} == "vk" ]]
then
	reducerfile="uniq_filter.py"
elif [[ ${datatype} == "twitter" ]]
then
	reducerfile="uniq_filter_twt.py"
fi

input="/user/ime/wangzehui/corpus/$1/*/part*"
output="/user/ime/fengchaobing/dl_corpus/$1/uniq_postid/"

hadconf="/etc/hadoop1.0/conf"
hstream="/usr/local/hadoop1.0/contrib/streaming/hadoop-streaming-0.20.2-cdh3u4.jar"

hadoop jar ${hstream}\

hadoop fs -rmr ${output}
hadoop jar ${hstream} \
    -D mapred.job.name="uniq_postid, ${datatype}, fengchaobing" \
    -D mapred.job.priority="VERY_HIGH" \
    -D mapred.map.tasks=500 \
    -D mapred.reduce.tasks=100 \
    -D stream.num.map.output.key.fileds=1 \
    -D mapred.text.key.partitioner.options="-k1,1" \
    -D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
    -D mapred.text.key.comparator.options="-k1,1" \
    -input "${input}" \
    -output "${output}" \
    -file "${reducerfile}" \
    -mapper "cat" \
    -reducer "python ${reducerfile}" \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner
