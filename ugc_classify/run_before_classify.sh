#datatype="facebook"
#datatype="instagram"
#datatype="twitter"

#lang="es"

#cd freq_vob && sh run.sh ${datatype} ${lang}
#cd ../trans_vob && sh run.sh ${datatype} ${lang}

#cd .. && sh ugc_classify_hadoop.sh ${datatype} ${lang}

if false
then
#proccessing ru :

lang="ru"

datatype="facebook"
cd freq_vob && sh run.sh ${datatype} ${lang}
cd ../trans_vob && sh run.sh ${datatype} ${lang}

datatype="instagram"
cd ../freq_vob && sh run.sh ${datatype} ${lang}
cd ../trans_vob && sh run.sh ${datatype} ${lang}

datatype="twitter"
cd ../freq_vob && sh run.sh ${datatype} ${lang}
cd ../trans_vob && sh run.sh ${datatype} ${lang}

datatype="vk"
cd ../freq_vob && sh run.sh ${datatype} ${lang}
cd ../trans_vob && sh run.sh ${datatype} ${lang}
fi

#proccessing pt :

lang="pt"

datatype="facebook"
cd freq_vob && sh run.sh ${datatype} ${lang}
cd ../trans_vob && sh run.sh ${datatype} ${lang}

datatype="instagram"
cd ../freq_vob && sh run.sh ${datatype} ${lang}
cd ../trans_vob && sh run.sh ${datatype} ${lang}

datatype="twitter"
cd ../freq_vob && sh run.sh ${datatype} ${lang}
cd ../trans_vob && sh run.sh ${datatype} ${lang}

cd ..
sh tar_update.sh 

