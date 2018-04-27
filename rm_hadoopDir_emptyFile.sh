dir=$1
datatype=$2

fsdufile="./fsdu_${2}.txt"
fsdu=`hadoop fs -du ${dir}`

echo "${fsdu}" > ${fsdufile}
delete_filelist=`awk '/^0/ {print $2}' ${fsdufile}`

for file in ${delete_filelist}
do
	echo /${file#*//*/}
	hadoop fs -rmr /${file#*//*/}
done

rm ${fsdufile}
