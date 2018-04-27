facebook_es_top_freq_10000.txt #fb_es 前10000条记录

facebook_es_top_freq_1000.txt #fb_es 前1000条记录

es_fb_ugc_part.txt #es_fb ugc部分。 由于编辑没有考虑重复

es_fb_ugc.txt #es_fb ugc部分。 从top1000中， 按照和 es_fb_ugc_part.txt 相似度判定进行扩展

es_fb_no_ugc.txt #es_fb 非ugc部分

pred_facebook_es_top_freq_10000_iter1_20180408.txt #第一轮迭代输出 ugc top10000

pred_facebook_es_top_freq_1000_iter1_20180408.txt #第一轮迭代输出 ugc top1000

pred_facebook_es_top_freq_1000_iter1_20180408_ugc.txt #第一轮迭代输出 ugc top1000, 经过es编辑标注后的， ugc

pred_facebook_es_top_freq_1000_iter1_20180408_no_ugc.txt #第一轮迭代输出 ugc top1000, 经过es编辑标注后的， no_ugc

#整合、修正正负样例

新正：pred_facebook_es_top_freq_1000_iter1_20180408_ugc.txt

新负：pred_facebook_es_top_freq_1000_iter1_20180408_no_ugc.txt + es_fb_no_ugc_iter1.txt - pred_facebook_es_top_freq_1000_iter1_20180408_ugc.txt

将之前正 负训练， 增加后缀iter1. 生成新的 正 负训练

es_fb_ugc_before_repair.txt #es_fb ugc 修复前状态； 第一次迭代， 正负 训练调整后的状态

es_fb_no_ugc_before_repair.txt

es编辑 修复

pred_facebook_es_top_freq_1000_iter2_20180410.txt #第二轮迭代输出 ugc top1000。 训练集中的 正例全部预测成功。其余的 也基本都是， 应该 97、8%准确率

es_fb_ugc_repair.txt es_fb_no_ugc_repair.txt #修复后正负， 也是第二轮迭代的 训练集

es_fb_1000lines.txt #随机抽取 低频部分1000条

es_fb_1000lines_ugc.txt es_fb_1000lines_no_ugc.txt #低频部分1000条 标注结果

新的训练集正负：repair 和 1000lines的直接合并

