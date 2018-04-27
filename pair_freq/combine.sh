datatype=$1
lang=$2
begin=$3
end=$4

output_dir="pair_freq_${lang}_output"

combine_output="${output_dir}/${datatype}_${lang}_pair_freq_${begin}_${end}.txt"
rm_app_output="${output_dir}/${datatype}_${lang}_pair_freq_rm_app.txt"
format_output="${output_dir}/${datatype}_${lang}_pair_freq_format.txt"

rm -f ${combine_output} ${rm_app_output} ${format_output}

for((i=$3; i<$4; i+=100))
do
    cat "${output_dir}/${datatype}_${lang}_pair_freq_${i}_$[${i}+100].txt" >> "${combine_output}"
    #cat "${datatype}_${lang}_pair_sentence_freq_${i}_$[${i}+100].txt" >> "${datatype}_${lang}_pair_sentence_freq_${begin}_${end}.txt"
done

python remove_appro.py ${combine_output} > ${rm_app_output}

python format_output.py ${rm_app_output} > ${format_output}
