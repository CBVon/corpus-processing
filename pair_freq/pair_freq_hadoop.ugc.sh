#!/bin/bash
source /etc/profile
source ~/.bash_profile

hadoopcmd=`which hadoop`
hadconf="/etc/hadoop1.0/conf"
hstream="/usr/local/hadoop1.0/contrib/streaming/hadoop-streaming-0.20.2-cdh3u4.jar"

datatype=$1
lang=$2
begin=$3
end=$4
pairtxt=""

input1=""
input2=""
input3=""
output=""

if [[ ${lang} == "id" ]]
then
    pairtxt="Id_word_pairs.txt"
elif [[ ${lang} == "pt" ]]
then
    pairtxt="Pt_word_pairs.txt"
fi

pairfreqfile="./pair_freq_${lang}_output/${datatype}_${lang}_pair_freq_${3}_${4}.txt"

if [[ ${datatype} == "ugc" ]]
then
#input="/user/ime/fengchaobing/dl_corpus/$1/lang_divide/$2/part-*"

input1="/user/ime/fengchaobing/dl_corpus/facebook/lang_divide/$2/part-*"
input2="/user/ime/fengchaobing/dl_corpus/instagram/lang_divide/$2/part-*"
input3="/user/ime/fengchaobing/dl_corpus/twitter/lang_divide/$2/part-*"
output="/user/ime/fengchaobing/dl_corpus/$1/pair_freq/$2/$3"

#input1="/user/gime/fengchaobing/dl_corpus/facebook/lang_divide/$2/part-*"
#input2="/user/gime/fengchaobing/dl_corpus/instagram/lang_divide/$2/part-*"
#input3="/user/gime/fengchaobing/dl_corpus/twitter/lang_divide/$2/part-*"
#output="/user/gime/fengchaobing/dl_corpus/$1/pair_freq/$2/$3"
fi

rm -rf ${pairfreqfile}
for ((i=$3; i<$4; ++i))
do
c1=`awk -F'\t' 'NR=="'"$[$i+1]"'"{print $1}' ${pairtxt}`
c2=`awk -F'\t' 'NR=="'"$[$i+1]"'"{print $2}' ${pairtxt}`
c3=`awk -F'\t' 'NR=="'"$[$i+1]"'"{print $3}' ${pairtxt}`
c4_=`awk -F'\t' 'NR=="'"$[$i+1]"'"{print $4}' ${pairtxt}`
c4=${c4_:0:-1}

if [[ ${#c1} == "0" || ${#c2} == "0" || ${#c3} == "0" || ${#c4} == "0"  ]]
then
#    echo "continue----- -----4" >> ${pairfreqfile}
    continue
fi
echo $i, ${c3}, ${c4}
echo -e "#${c3},\t${c4}" >> ${pairfreqfile}

$hadoopcmd --config "$hadoopconf" fs -rmr ${output};
$hadoopcmd --config "$hadoopconf" jar "$hstream" \
    -D mapred.job.name="pair_freq_hadoop.ugc, ${datatype}, ${lang}, ${begin}, fengchaobing" \
    -D mapred.job.priority="VERY_HIGH" \
    -D mapred.map.tasks=500 \
    -D mapred.reduce.tasks=1 \
    -D stream.num.map.output.key.fields=2 \
    -D mapred.output.key.comparator.class=org.apache.hadoop.mapred.lib.KeyFieldBasedComparator   \
    -D mapred.text.key.comparator.options="-k2,2nr -k1,1" \
    -file "filter_map.py" \
    -file ${pairtxt} \
    -mapper "python filter_map.py ${pairtxt}  $i 2 3" \
    -reducer "cat" \
    -input ${input1} \
    -input ${input2} \
    -input ${input3} \
    -output ${output} \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner
${hadoopcmd} fs -cat "${output}/part-00000" | head -50 >> ${pairfreqfile}
#echo "process----- -----4" >> ${pairfreqfile}
done
