#!/bin/bash
source /etc/profile
source ~/.bash_profile

hadoopcmd=`which hadoop`
hadconf="/etc/hadoop1.0/conf"
hstream="/usr/local/hadoop1.0/contrib/streaming/hadoop-streaming-0.20.2-cdh3u4.jar"

#lang=$1
#ugc_langs=("id" "es" "ru" "pt" "fr" "de")
ugc_langs=("de")

for lang in ${ugc_langs[@]}
do
input1="/user/ime/fengchaobing/dl_corpus/facebook/lang_divide/${lang}/part-*"
input2="/user/ime/fengchaobing/dl_corpus/instagram/lang_divide/${lang}/part-*"
input3="/user/ime/fengchaobing/dl_corpus/twitter/lang_divide/${lang}/part-*"
output_tmp="/user/ime/fengchaobing/dl_corpus/ugc/lang_divide_tmp/${lang}"
output="/user/ime/fengchaobing/dl_corpus/ugc/lang_divide/${lang}"

if [[ ${lang} != "ru" ]]
then
$hadoopcmd --config "$hadoopconf" fs -rmr ${output_tmp};
$hadoopcmd --config "$hadoopconf" jar "$hstream" \
    -D mapred.job.name="combine_ugc_from_langdivide_hadoop_tmp, ${lang}, fengchaobing" \
    -D mapred.job.priority="VERY_HIGH" \
    -D mapred.map.tasks=500 \
    -D mapred.reduce.tasks=100 \
    -D stream.num.map.output.key.fields=1 \
    -D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator   \
    -D mapred.text.key.comparator.options="-k1,1" \
    -file filter_map.py \
    -file freq_reduce.py \
    -mapper "python filter_map.py" \
    -reducer "python freq_reduce.py" \
    -input ${input1} \
    -input ${input2} \
    -input ${input3} \
    -output ${output_tmp} \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner
elif [[ ${lang} == "ru" ]]
then
input4="/user/ime/fengchaobing/dl_corpus/vk/lang_divide/${lang}/part-*"
$hadoopcmd --config "$hadoopconf" fs -rmr ${output_tmp};
$hadoopcmd --config "$hadoopconf" jar "$hstream" \
    -D mapred.job.name="combine_ugc_from_langdivide_hadoop_tmp, ${lang}, fengchaobing" \
    -D mapred.job.priority="VERY_HIGH" \
    -D mapred.map.tasks=500 \
    -D mapred.reduce.tasks=100 \
    -D stream.num.map.output.key.fields=1 \
    -D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator   \
    -D mapred.text.key.comparator.options="-k1,1" \
    -file filter_map.py \
    -file freq_reduce.py \
    -mapper "python filter_map.py" \
    -reducer "python freq_reduce.py" \
    -input ${input1} \
    -input ${input2} \
    -input ${input3} \
    -input ${input4} \
    -output ${output_tmp} \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner
fi

$hadoopcmd --config "$hadoopconf" fs -rmr ${output};
$hadoopcmd --config "$hadoopconf" jar "$hstream" \
    -D mapred.job.name="combine_ugc_from_langdivide_hadoop, ${lang}, fengchaobing" \
    -D mapred.job.priority="VERY_HIGH" \
    -D mapred.map.tasks=500 \
    -D mapred.reduce.tasks=1 \
    -D stream.num.map.output.key.fields=2 \
    -D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator   \
    -D mapred.text.key.comparator.options="-k2,2nr -k1,1" \
    -mapper cat \
    -reducer cat \
    -input ${output_tmp} \
    -output ${output} \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner

${hadoopcmd} fs -cat "${output}/part-00000" | head -10000 > "./top_freq_output/ugc_${lang}_top_freq_10000.txt"
done
