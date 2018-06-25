#!/bin/bash
#sh origin_QApairs_hadoop.sh facebook
source /etc/profile
source ~/.bash_profile

hadoopcmd=`which hadoop`
hadconf="/etc/hadoop1.0/conf"
hstream="/usr/local/hadoop1.0/contrib/streaming/hadoop-streaming-0.20.2-cdh3u4.jar"

datatype=$1

if [[ ${datatype} == "facebook" ]]
then
input="/user/ime/corpus/${datatype}/201*/201*/${datatype}_detail_2*.txt"
mapfile="filter_map_for_fb.py"
elif [[ ${datatype} == "instagram" ]]
then
input="/user/ime/corpus/${datatype}/201*/201*/${datatype}_detail_post_2*.txt"
mapfile="filter_map_for_ins.py"
fi

output="/user/ime/fengchaobing/dl_corpus/${datatype}/get_QApairs/origin_QApairs"

$hadoopcmd --config "$hadoopconf" fs -rmr ${output}
$hadoopcmd --config "$hadoopconf" jar "$hstream" \
    -D mapred.job.name="get_QApairs, ${datatype}, fengchaobing" \
    -D mapred.job.priority="HIGH" \
    -D mapred.map.tasks=10000 \
    -D mapred.reduce.tasks=100 \
    -file ${mapfile} \
    -input ${input} \
    -output ${output} \
    -mapper "python ${mapfile}"\
    -reducer "cat"

