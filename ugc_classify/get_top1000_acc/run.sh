# sh run.sh de facebook
lang=$1
datatype=$2

echo "get ugc_top1000 file......"
#hadoop fs -cat /user/ime/fengchaobing/dl_corpus/${datatype}/ugc_classify/${lang}/part-00000 | head -n 1000 > ${lang}/${lang}_${datatype}_top1000
hadoop fs -cat /user/ime/fengchaobing/dl_corpus/${datatype}/ugc_classify/${lang}/part-00000 | head -n 500 > ${lang}/${lang}_${datatype}_top1000

python get_acc.py ${lang} ${datatype}
