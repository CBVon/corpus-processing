#!/bin/bash
source /etc/profile
source ~/.bash_profile

hadoopcmd=`which hadoop`
hadconf="/etc/hadoop1.0/conf"
hstream="/usr/local/hadoop1.0/contrib/streaming/hadoop-streaming-0.20.2-cdh3u4.jar"

datatype=$1
lang=$2
input=""
if [[ ${lang} == "tl" ]]
then
    input="/user/gime/DaBaiGouGIME/DaBaiGouGIMENGramST/*text*{2017{10,11,12},2018{01,02,03}}*"
fi

output="/user/ime/fengchaobing/dl_corpus/${datatype}/format_transform_201710_201803/"
mapperfile=""
reducerfile=""

if [[ ${datatype} == "facebook" || ${datatype} == "instagram" || ${datatype} == "twitter" || ${datatype} == "vk" ]]
then
	input="/user/ime/fengchaobing/dl_corpus/$1/uniq_postid/part-*"
	#input="/user/ime/fengchaobing/dl_corpus/$1/uniq_postid/part-00000"
    mapperfile="corpus_process_map_ugc.py"
	reducerfile="stat_reducer_ugc.py"
elif [[ ${datatype} == "dbg_pinjie" ]]
then
	input="/user/gime/DaBaiGouGIME/DaBaiGouGIMENGram/*text*"
    mapperfile="corpus_process_map_dbg.py"
	reducerfile="stat_reducer_dbg.py"
elif [[ ${datatype} == "dbg_st" ]]
then
#*********************************************************************************************************************************************************
	#input="/user/gime/DaBaiGouGIME/DaBaiGouGIMENGramST/*text*"
    #input="/user/gime/DaBaiGouGIME/DaBaiGouGIMENGramST/ngramST.ugm.dbg.typany.20180307.txt"
	mapperfile="corpus_process_map_dbg.py"
	reducerfile="stat_reducer_dbg.py"
fi

$hadoopcmd --config "$hadoopconf" fs -rmr ${output}
$hadoopcmd --config "$hadoopconf" jar "$hstream" \
	-D mapred.job.name="format transform, ${datatype}, fengchaobing" \
    -D mapred.job.priority="VERY_HIGH" \
	-D stream.num.map.output.key.fields=2 \
	-D mapred.text.key.partitioner.options="-k1,2" \
	-D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator \
	-D mapred.text.key.comparator.options="-k1,1 -k2,2" \
	-D mapred.map.tasks=500 \
	-D mapred.reduce.tasks=100 \
    -cacheArchive hdfs://master01.zeus.hadoop.ctc.sogou-op.org:6230/user/ime/wangzehui/language_detect/demo_for_format.tar.gz#demo_for_format \
    -mapper "python ${mapperfile}" \
	-reducer "python ${reducerfile}" \
    -file "${mapperfile}" \
    -file "${reducerfile}" \
    -file "vocab_no.txt" \
    -file "lite.wordlist.wFacebookNDabaigouFreq.txt" \
	-input ${input} \
	-output ${output} \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner 

