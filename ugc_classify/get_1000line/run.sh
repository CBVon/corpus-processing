#sh get_1000line.sh twitter es

#datatype="facebook"
#datatype="instagram"
#datatype="twitter"
datatype="vk"

short_d=""
if [[ ${datatype} == "facebook" ]]
then
    short_d="fb"
elif [[ ${datatype} == "instagram" ]]
then
    short_d="ins"
elif [[ ${datatype} == "twitter" ]]
then
    short_d="twt"
elif [[ ${datatype} == "vk" ]]
then
    short_d="vk"
fi

lang="ru"
#lang="pt"
#lang="fr"
#lang="de"

sh get_1000line_hadoop.sh ${datatype} ${lang}
hadoop fs -cat /user/ime/fengchaobing/dl_corpus/${datatype}/get_1000line/${lang}/part-00000 > ${lang}/${lang}_${short_d}_1000lines.txt 


