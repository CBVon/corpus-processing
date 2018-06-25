lang="ru"
#lang="es"
#lang="fr"

#lang="it"
#lang="tl"
#lang="de"

#sh verb_extract_hadoop.sh pt
sh verb_extract_hadoop.sh "${lang}"

hadoop fs -cat /user/ime/fengchaobing/dl_corpus/ugc_dbg/verb_extract/${lang}/part-00000 > output/${lang}_verb_extract 
