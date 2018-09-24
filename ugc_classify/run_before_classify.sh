#datatype="facebook"
#datatype="instagram"
#datatype="twitter"

#lang="es"

#cd freq_vob && sh run.sh ${datatype} ${lang}
#cd ../trans_vob && sh run.sh ${datatype} ${lang}

#cd .. && sh ugc_classify_hadoop.sh ${datatype} ${lang}

if false
then
#processing ru :

lang="ru"
echo "processing ${lang} !"
datatype="facebook"
echo "processing ${lang} - ${datatype} !"
cd freq_vob && sh run.sh ${datatype} ${lang}
cd ../trans_vob && sh run.sh ${datatype} ${lang}

datatype="instagram"
echo "processing ${lang} - ${datatype} !"
cd ../freq_vob && sh run.sh ${datatype} ${lang}
cd ../trans_vob && sh run.sh ${datatype} ${lang}

datatype="twitter"
echo "processing ${lang} - ${datatype} !"
cd ../freq_vob && sh run.sh ${datatype} ${lang}
cd ../trans_vob && sh run.sh ${datatype} ${lang}

datatype="vk"
echo "processing ${lang} - ${datatype} !"
cd ../freq_vob && sh run.sh ${datatype} ${lang}
cd ../trans_vob && sh run.sh ${datatype} ${lang}
fi

if true
then
#processing pt :
#processing fr :
#processing de :

#lang="fr"
lang="de"
echo "processing ${lang} !"
datatype="facebook"
echo "processing ${lang} - ${datatype} !"
cd freq_vob && sh run.sh ${datatype} ${lang}
cd ../trans_vob && sh run.sh ${datatype} ${lang}

datatype="instagram"
echo "processing ${lang} - ${datatype} !"
cd ../freq_vob && sh run.sh ${datatype} ${lang}
cd ../trans_vob && sh run.sh ${datatype} ${lang}

datatype="twitter"
echo "processing ${lang} - ${datatype} !"
cd ../freq_vob && sh run.sh ${datatype} ${lang}
cd ../trans_vob && sh run.sh ${datatype} ${lang}
fi



cd ..
sh tar_update.sh 

