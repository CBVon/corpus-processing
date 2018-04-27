场景背景：
	本脚本主要是用来针对Typany语料进行语言检测。
NOTICE!
	本脚本处理情况不区分细分语种，例如巴葡和葡葡；加拿大法语和法语等；

检测方法：
	针对语料输入不长，且需要在hadoop上执行的情况，使用distance模型进行检测。

使用方法：
	执行corpus_run.sh脚本即可。
	修改内容：
	1. mapred.map.tasks----指定脚本的map数；
	2. mapred.reduce.tasks----指定脚本的reduce数；
	3. input----需要进行语言检测的hdfs目录
	4. out----执行语言检测的输出目录
	5. mapred.job.name----本次脚本的名字。

Input格式：
	每行一个待检测句子。如text\n。
Output格式：
	每行一个待检测句子+语言标签。如text\tLANG\n。
