datatype=$1
lang=$2

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

#python markov_2gram_vob.py ../origin_corpus/es_fb_no_ugc.txt es_fb_no_ugc_trans_vob.pkl

python markov_2gram_vob.py ../origin_corpus/${lang}_${short_d}_no_ugc.txt ${lang}_${short_d}_no_ugc_trans_vob.pkl
