#coding: utf-8
#python count.py es facebook
import sys
import numpy as np
import cPickle
import math
import random
import re


from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn import metrics
from sklearn.metrics import classification_report

#python count.py es facebook
lang = sys.argv[1]
datatype = ""
if sys.argv[2] == "facebook":
    datatype = "fb"
elif sys.argv[2] == "instagram":
    datatype = "ins"
elif sys.argv[2] == "twitter":
    datatype = "twt"

nfilter_str = "pega esto en|pega en|Ver más|pide un deseo|ya estoy muerto y no tenia amigos|di tu nombre|si no pones esto en|si no pegas esto en" #fb-es-no_ugc
nfilter_str = "HASTA LA PRÓXIMA MENCIÓN|Gracias por compartir tus fotos|Fotos antiguas|Old pics|FOTO DEL DÍA|PHOTO OF THE DAY|Whatsapp|whatsapp|WHATSAPP|Más detalles en|www.|Sigue a @" \
"|Para tus fotos antiguas|For your old Pics|Sigueme y te sigo|youtube.|PONER DONDE HICISTE FOTO|La vida en un CLICK|SEGUIR|FOLLOW|000 ENVÍOS|000 Envio" \
"|Para leer la nota completa|Chosen by|Foto seleccionada por|Por favor sigue|Please follow|Damos la enhorabuena a|SÓLO FOTOS HECHAS POR TI|ONLY PHOTOS TAKEN BY YOURSELF" #ins-es-no_ugc
nfilter_str = "Publiqué una nueva foto en Facebook|No me han retwitteado ningún Tweet últimas 24h|He publicado una foto nueva en Facebook|He empezado un streaming en directo en @YouTube" \
"|vía @YouTube|via @YouTube|vía @|Disponible en App Store y en Google Play|No te lo pierdas|RT|Pregúntame o cuéntame algo|Descubre el tuyo en|Confira este check-in épico no @Swarmapp" \
"si te gusta dale like y suscribete al canal|a través de @YouTube|NUEVO VÍDEO|Echa un vistazo a mi transmisión desde mi PlayStation 4|sucríbete a este canal" \
"Inicié una transmisión en directo en @YouTube|Mi Tweet más retwitteado 2 RTs últimas 24h|He descubierto a que emoticono del whatsapp me parezco en lo clava|Nos das un RT|50 de Descuento" \
"Más en|No os lo perdáis|Únete a mí|whatsapp|Participa aquí|Mi personaje de The Big Bang Theory|Vota aquí" #twt-es-no_ugc
es_filter_str = "pega esto en|pega en|Ver más|pide un deseo|ya estoy muerto y no tenia amigos|di tu nombre|si no pones esto en|si no pegas esto en" \
"HASTA LA PRÓXIMA MENCIÓN|Gracias por compartir tus fotos|Fotos antiguas|Old pics|FOTO DEL DÍA|PHOTO OF THE DAY|Whatsapp|whatsapp|WHATSAPP|Más detalles en|www.|Sigue a @" \
"|Para tus fotos antiguas|For your old Pics|Sigueme y te sigo|youtube.|PONER DONDE HICISTE FOTO|La vida en un CLICK|SEGUIR|FOLLOW|000 ENVÍOS|000 Envio" \
"|Para leer la nota completa|Chosen by|Foto seleccionada por|Por favor sigue|Please follow|Damos la enhorabuena a|SÓLO FOTOS HECHAS POR TI|ONLY PHOTOS TAKEN BY YOURSELF" \
"Publiqué una nueva foto en Facebook|No me han retwitteado ningún Tweet últimas 24h|He publicado una foto nueva en Facebook|He empezado un streaming en directo en @YouTube" \
"|vía @YouTube|via @YouTube|vía @|Disponible en App Store y en Google Play|No te lo pierdas|RT|Pregúntame o cuéntame algo|Descubre el tuyo en|Confira este check-in épico no @Swarmapp" \
"si te gusta dale like y suscribete al canal|a través de @YouTube|NUEVO VÍDEO|Echa un vistazo a mi transmisión desde mi PlayStation 4|sucríbete a este canal" \
"Inicié una transmisión en directo en @YouTube|Mi Tweet más retwitteado 2 RTs últimas 24h|He descubierto a que emoticono del whatsapp me parezco en lo clava|Nos das un RT|50 de Descuento" \
"Más en|No os lo perdáis|Únete a mí|whatsapp|Participa aquí|Mi personaje de The Big Bang Theory|Vota aquí" #combine-es-no_ugc

filter_str = ""
if lang == "es":
    filter_str = es_filter_str

def get_filter_flag(sent):
    filter_flag = 0
    for term in filter_str.split("|"):
        if term in sent:
            #print "sent : " + sent
            filter_flag += 1
    return filter_flag


ugc_all = [i.strip() for i in open("./freq_vob/" + lang + "_" + datatype + "_ugc_vob.txt", "r").readlines()] #s    f
no_ugc_all = [i.strip() for i in open("./freq_vob/" + lang + "_" + datatype + "_no_ugc_vob.txt", "r").readlines()]
u_all = [i.split('\t')[0] for i in ugc_all] #s
no_u_all = [i.split('\t')[0] for i in no_ugc_all]

#print "len(u_all) : " + str(len(u_all)) #正例数目
#print "len(no_u_all) : " + str(len(no_u_all)) #负例数目
inter_u = list(set(u_all).intersection(set(no_u_all))) #正负例-交集数目
#print "len(inter_u) : " + str(len(inter_u)) #交集较小，约 1/10 占比
ugc_vob = [i for i in ugc_all if i.split('\t')[0] not in inter_u][:100]
no_ugc_vob = [i for i in no_ugc_all if i.split('\t')[0] not in inter_u][:100]
#print "len(ugc_vob) : " + str(len(ugc_vob)) #纯正例数目
#print "len(no_ugc_vob) : " + str(len(no_ugc_vob)) #纯负例数目
ugc_dict = {i.split('\t')[0]:int(i.split('\t')[1]) for i in ugc_vob}
no_ugc_dict = {i.split('\t')[0]:int(i.split('\t')[1]) for i in no_ugc_vob}


#获取词频分数(语句内容， 词-频字典)
def get_word_freq_score(sent, _dict):
    word_freq_score = 0.0
    sent_list = sent.split(' ')
    for word in sent_list:
        if _dict.has_key(word):
            #print word, sent
            word_freq_score += _dict[word]
    return word_freq_score


trans_dict = cPickle.load(open("./trans_vob/" + lang + "_" + datatype + "_no_ugc_trans_vob.pkl", "r"))


#获取马尔科夫-2gram-转移概率。关键特征
def get_markov_score(sent):
    markov_score = 0.0
    sent_list = sent.split(' ')
    pre_word = None
    for word in sent_list:
        if pre_word == None:
            if trans_dict["bbbegin"].has_key(word):
                markov_score += math.log(trans_dict["bbbegin"][word])
            else:
                markov_score += math.log(trans_dict["bbbegin"]["ooothers"])
        elif pre_word != None:
            if tran_dict[preword].has_key(word):
                markov_score += math.log(trans_dict[pre_word][word])
            else:
                markov_score += math.log(trans_dict[pre_word]["ooothers"])
    return markov_score


#reg = re.compile(u"[.!?;&#]+")
reg = re.compile(u"[\.!\?;&#\+\-\*\\/]+")

#获取特征 line→feat_vector
def get_feat(line):
    line = line.strip()
    sent = line.split('\t')[0]
    f = int(line.split('\t')[1])
    
    filter_flag = get_filter_flag(sent)

    line_len = len(line)
    words_num = len(line.split(' '))
    avg_word_len = float(line_len) / words_num
    
    up_chars_num = 0
    amaze_num = 0
    doubt_num = 0
    for c in line:
        if c >= 'A' and c <= 'Z':
            up_chars_num += 1
        if c == '!':
            amaze_num += 1
        if c == '?':
            doubt_num += 1

    sub_line = re.sub(reg, "", line).strip()
    #is_bigger_2 = 0 #words_len, 引入此特征， 会让结果稍微变差。 编辑对是否>2没有固定的规律。 如果后续训练需要>2，就直接使用条件过滤即可
    if len(sub_line.split(' ')) > 2:
        is_bigger_2 = 1

    markov_score = get_markov_score(sent) #只针对 非ugc计算
    ugc_word_freq_score = get_word_freq_score(sent, ugc_dict) #for ugc
    no_ugc_word_freq_score = get_word_freq_score(sent, no_ugc_dict) #for no_ugc

    return [f, filter_flag, \
    line_len, words_num, avg_word_len, 
    up_chars_num, float(up_chars_num) / words_num, 
    amaze_num, float(amaze_num) / words_num, 
    doubt_num, float(doubt_num) / words_num, \
    #is_bigger_2, 
    markov_score, float(markov_score) / words_num, 
    ugc_word_freq_score, float(ugc_word_freq_score) / words_num, 
    no_ugc_word_freq_score, float(no_ugc_word_freq_score) / words_num]
    #20180402实验证明： 多filter_flag*5 拼接并不能使结果变好
    #20180403实验证明：只利用avg类型要特征 比同时利用 avg和count 效果要差一点点点
    """
    return [f, filter_flag, \
    line_len, words_num, avg_word_len, 
    float(up_chars_num) / words_num, 
    float(amaze_num) / words_num, 
    float(doubt_num) / words_num, \
    float(markov_score) / words_num, 
    float(ugc_word_freq_score) / words_num, 
    float(no_ugc_word_freq_score) / words_num]
    """


#获取训练集xy
def get_train_xy(file, y):
    train_file = open(file, "r")
    train_list = train_file.readlines()
    train_xy = []
    for line in train_list:
        if len(line.strip().split('\t')) != 2:
            continue

        line_x = get_feat(line)
        line_y = [y]
        line_xy = line_x + line_y
        train_xy.append(line_xy)
    return train_xy


train_posi_xy = get_train_xy("./origin_corpus/" + lang + "_" + datatype + "_ugc.txt", 1)
train_nega_xy = get_train_xy("./origin_corpus/" + lang + "_" + datatype + "_no_ugc.txt", 0)
train_xy = train_posi_xy + train_nega_xy
#恒定——随机打乱
random.seed(0) 
random.shuffle(train_xy)
train_xy = np.array(train_xy)
#print train_xy.shape #(1000, 18)

#train_1000
train_x = train_xy[: , : -1]
train_y = train_xy[: , -1]
#print "sum(train_y) : " + str(sum(train_y)) #523.0

standard_scaler = preprocessing.StandardScaler().fit(train_x)
train_x = standard_scaler.transform(train_x)

min_max_scaler = preprocessing.MinMaxScaler().fit(train_x)
train_x = min_max_scaler.transform(train_x)

normalizer = preprocessing.Normalizer().fit(train_x)
train_x = normalizer.transform(train_x)
#RF
rf = RandomForestClassifier(n_estimators=100, oob_score=True, random_state=0)
rf.fit(train_x, train_y)

print "feature : [f, filter_flag, line_len, words_num, avg_word_len, up_chars_num, float(up_chars_num) / words_num, amaze_num, float(amaze_num) / words_num, doubt_num, float(doubt_num) / words_num," \
"markov_score, float(markov_score) / words_num, ugc_word_freq_score, float(ugc_word_freq_score) / words_num, no_ugc_word_freq_score, float(no_ugc_word_freq_score) / words_num, y]"
print "rf.feature_importances_ : " + str(rf.feature_importances_)

#袋外分数（理解为袋外数据作为验证集时的准确率，也就是模型的泛化能力）
print "rf.oob_score_ : " + str(rf.oob_score_) #rf.oob_score_ : 0.955 #包外估计评分

pred_prob_y = rf.predict_proba(train_x)[: , 1] 
pred_train_y = rf.predict(train_x)
print "AUC Score (prob) : " + str(metrics.roc_auc_score(train_y,pred_prob_y))  #AUC Score (train_x) : 1.0 #自身学习结果
print "AUC Score (0-1) : " + str(metrics.roc_auc_score(train_y,pred_train_y))
#pred_y = [int(i > 0.5) for i in pred_prob_y] #0.5是阈值， 控制正负例
#print "F1 Score (train_x) : " + str(metrics.f1_score(train_y,pred_y))

pred_y = rf.predict(train_x)
print "classification_report(train_y, pred_y) : \n" + str(classification_report(train_y, pred_y))
#print "F1 Score (train_x) : " + str(metrics.f1_score(train_y,pred_y))

'''
#打印 正负样例分别的均值
print "[f, filter_flag, line_len, words_num, avg_word_len, up_chars_num, float(up_chars_num) / words_num, amaze_num, float(amaze_num) / words_num, doubt_num, float(doubt_num) / words_num," \
"markov_score, float(markov_score) / words_num, ugc_word_freq_score, float(ugc_word_freq_score) / words_num, no_ugc_word_freq_score, float(no_ugc_word_freq_score) / words_num, y]"
print np.mean(train_posi_xy, axis=0)
print np.mean(train_nega_xy, axis=0)
'''

"""
********** ********** ********** ********** ********** ********** ********** ********** ********** **********
********** ********** ********** ********** ********** ********** ********** ********** ********** **********
********** ********** ********** ********** ********** ********** ********** ********** ********** **********
"""
#train_500 test_500
print "//********** **********//"
test_xy = train_xy[int(len(train_xy) * 0.5): ]
train_xy = train_xy[: int(len(train_xy) * 0.5)]
#print train_xy.shape #(500, 18)
#print test_xy.shape #(500, 18)

train_x = train_xy[: , : -1]
train_y = train_xy[: , -1]
test_x = test_xy[: , : -1]
test_y = test_xy[: , -1]
#print "sum(train_y) : " + str(sum(train_y)) #262
#print "sum(test_y) : " + str(sum(test_y)) #261

standard_scaler = preprocessing.StandardScaler().fit(train_x)
train_x = standard_scaler.transform(train_x)

min_max_scaler = preprocessing.MinMaxScaler().fit(train_x)
train_x = min_max_scaler.transform(train_x)

normalizer = preprocessing.Normalizer().fit(train_x)
train_x = normalizer.transform(train_x)

test_x = standard_scaler.transform(test_x)
test_x = min_max_scaler.transform(test_x)
test_x = normalizer.transform(test_x)
#RF
print "RF : ***** *****"
rf = RandomForestClassifier(n_estimators=500, oob_score=True, random_state=0, class_weight="balanced")
#rf = RandomForestClassifier(n_estimators=500, oob_score=True, random_state=0)
rf.fit(train_x, train_y)

print "feature : [f, filter_flag, line_len, words_num, avg_word_len, up_chars_num, float(up_chars_num) / words_num, amaze_num, float(amaze_num) / words_num, doubt_num, float(doubt_num) / words_num," \
"markov_score, float(markov_score) / words_num, ugc_word_freq_score, float(ugc_word_freq_score) / words_num, no_ugc_word_freq_score, float(no_ugc_word_freq_score) / words_num, y]"
print "rf.feature_importances_ : " + str(rf.feature_importances_)

pred_test_y = rf.predict(test_x)
print "classification_report(train_y, pred_y) : \n" + str(classification_report(test_y, pred_test_y))
print "F1 Score (train_x) : " + str(metrics.f1_score(test_y,pred_test_y)) #只针对正例 

#SVM
print "SVM : ***** *****"
svc = SVC()
svc.fit(train_x, train_y)
#'SVC' object has no attribute 'feature_importances_'
pred_test_y = svc.predict(test_x)
print "classification_report(train_y, pred_y) : \n" + str(classification_report(test_y, pred_test_y))
print "F1 Score (train_x) : " + str(metrics.f1_score(test_y,pred_test_y))


