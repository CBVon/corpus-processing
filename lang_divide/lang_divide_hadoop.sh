#!/bin/bash
source /etc/profile
source ~/.bash_profile

datatype=$1

#ugc_langs=("id" "es" "ru" "pt" "fr" "en" "de")
ugc_langs=("id" "es" "ru" "pt" "fr" "de" "it" "tl")
#ugc_langs=("it" "tl")

vk_langs=("ru")

#dbg_langs=("id" "es" "esUS" "esLAT" "ru" "ptBR" "pt" "frCA" "frFR" "en" "de")
#dbg_langs=("id" "es" "esUS" "esLAT" "ru" "ptBR" "pt" "frCA" "frFR" "de" "it" "tl")
#dbg_langs=("it" "tl")
#dbg_langs=("de")
dbg_langs=("id" "es" "esUS" "esLAT" "ru" "ptBR" "pt" "frCA" "frFR" "it" "tl")

langs=()
input="/user/ime/fengchaobing/dl_corpus/${datatype}/split_freq/part-*"
output_pre="/user/ime/fengchaobing/dl_corpus/${datatype}/lang_divide"

if [[ ${datatype} == "facebook" || ${datatype} == "instagram" || ${datatype} == "twitter" ]]
then
	langs=${ugc_langs[@]}
elif [[ ${datatype} == "dbg_st" || ${datatype} == "dbg_pinjie" ]]
then
	langs=${dbg_langs[@]}
elif [[ ${datatype} == "vk" ]]
then
    langs=${vk_langs[@]}
fi

for lang in ${langs[@]}
do	
	sh get_lang_data.sh ${datatype} ${lang} ${input} "${output_pre}/${lang}"
done
