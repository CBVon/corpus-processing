#!/bin/bash
#sh verb_extract_hadoop.sh pt
source /etc/profile
source ~/.bash_profile

hadoopcmd=`which hadoop`
hadconf="/etc/hadoop1.0/conf"
hstream="/usr/local/hadoop1.0/contrib/streaming/hadoop-streaming-0.20.2-cdh3u4.jar"

lang=$1
map_file="filter_map.py"
red_file="format_filter_reduce.py"
verb_file="${lang}2w_indict.verbchanged"

#input1="/user/ime/fengchaobing/dl_corpus/facebook/lang_divide/${lang}/part*"
#input2="/user/ime/fengchaobing/dl_corpus/instagram/lang_divide/${lang}/part*"
#input3="/user/ime/fengchaobing/dl_corpus/twitter/lang_divide/${lang}/part*"
input4="/user/ime/fengchaobing/dl_corpus/dbg_pinjie/lang_divide/${lang}/part*"
output="/user/ime/fengchaobing/dl_corpus/dbg_pinjie/verb_extract/${lang}/"

$hadoopcmd --config "$hadoopconf" fs -rmr ${output}
$hadoopcmd --config "$hadoopconf" jar "$hstream" \
    -D mapred.job.name="verb_extract, ${lang}, fengchaobing" \
    -D mapred.job.priority="VERY_HIGH" \
    -D mapred.map.tasks=10000 \
    -D mapred.reduce.tasks=1 \
    -D stream.num.map.output.key.fields=2 \
    -D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator   \
    -D mapred.text.key.comparator.options="-k2,2nr -k1,1" \
    -file ${map_file} \
    -file ${red_file} \
    -file ${verb_file} \
    -input ${input4} \
    -output ${output} \
    -mapper "python ${map_file} ${verb_file}" \
    -reducer "python ${red_file} ${verb_file}"

