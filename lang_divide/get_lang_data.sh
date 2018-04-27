#!/bin/bash
source /etc/profile
source ~/.bash_profile

hadoopcmd=`which hadoop`
hadconf="/etc/hadoop1.0/conf"
hstream="/usr/local/hadoop1.0/contrib/streaming/hadoop-streaming-0.20.2-cdh3u4.jar"

datatype=$1
lang=$2
input=$3
output=$4

$hadoopcmd --config "$hadoopconf" fs -rmr ${output}
$hadoopcmd --config "$hadoopconf" jar "$hstream" \
    -D mapred.job.name="lang_divide and freq_invert, ${datatype}, ${lang}, fengchaobing" \
    -D mapred.job.priority="VERY_HIGH" \
    -D mapred.map.tasks=500 \
    -D mapred.reduce.tasks=1 \
    -D stream.num.map.output.key.fields=2 \
    -D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator   \
    -D mapred.text.key.comparator.options="-k2,2nr -k1,1" \
    -input ${input} \
    -output ${output} \
    -file "filter_lang_map.py" \
    -mapper "python filter_lang_map.py ${lang}" \
    -reducer "cat"

#sh ../rm_hadoopDir_emptyFile.sh ${output} ${datatype}
${hadoopcmd} fs -cat "${output}/part-00000" | head -1000 > "./top_freq_output/${datatype}_${lang}_top_freq_1000.txt"
