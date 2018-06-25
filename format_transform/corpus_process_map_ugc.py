#! /usr/bin/python
# -*- coding: utf8 -*-
import sys
import codecs
import re
import glob


reload(sys)
sys.setdefaultencoding('utf-8')

inputfile = open('./vocab_no.txt','r')
inputlistfile = open('./lite.wordlist.wFacebookNDabaigouFreq.txt','r')


check_list = []
check_list_word = []
for vocab in inputfile:
    check_list.append(vocab.strip())

for line_word in inputlistfile:
    str_word = str(line_word).split('\t')[0]
    check_list_word.append(str_word)


def isnumeric(s):
    return all(c in "0123456789" for c in s)

def get_emoji():
    emoji_str = '﻿👵|👴|👷|👶|👱|👰|👳|👲|👽|👼|👿|✊|👹|👸|👻|👺|👥|👤|👧|👦|➕|☔|㊗|👢|👭|👬|👯|👮|👩|👨|👫|👪|🆖|🆗|🆔|🆕|🆒|🆓|👓|🆑|👝|👜|👟|👞|🆚|👘|🆘|🆙|👅|〰|👇|👆|👀|👃|👂|3⃣|👌|👏|👎|👉|👈|👋|🌃|🐵|🐴|🐷|🐶|🐱|🐰|🐳|🐲|🐽|🐼|🐾|🐹|🐸|🐻|🐺|🐥|🐤|🐧|🐦|🐡|🐠|🐣|🐢|🐭|🐬|🐯|🐮|🐩|🐨|🐫|🔐|🐕|🐔|🐗|🌍|🐑|🐐|🐓|🐒|🐝|🐜|🐟|🐞|🐙|🐘|🐛|🐚|🐅|🐄|🐇|🐆|🐁|🐀|🐃|🐂|🐍|🐌|🐏|🐎|🐉|🐈|🐋|👠|📵|📴|📷|📶|✅|👣|📳|📲|📼|📹|🚷|📻|📺|📥|📤|📧|🍵|📡|📠|📣|↖|📭|🚱|📯|📮|📩|📨|👡|📪|📕|📔|📗|📖|📑|📐|📓|📒|📝|📜|📟|🍱|📙|📘|📛|📚|📅|📄|📇|📆|📁|📀|📃|📂|📍|📌|📏|📎|📉|📈|📋|📊|💵|👕|💷|👾|💱|⛄|🅰|🅱|🅾|🅿|💿|💾|💹|👗|♏|💺|💥|💤|💧|👖|❕|⛔|💣|💢|💭|👑|💯|🍹|💩|💨|💫|👐|💕|🚥|💗|💖|💑|💐|💓|🍧|💝|💜|💟|👒|💙|♓|💛|💚|💅|💄|💇|💆|💁|💀|💃|💂|💍|💌|💏|💎|💉|💈|♿|◾|🚣|👙|🍡|🕥|🍮|🕧|🕦|🕡|✔|🕣|🚬|👚|⬜|🕕|🕔|🕗|🕖|🕑|🕐|🕓|👄|🕝|🚩|🕟|🕞|🕙|🕘|🕛|🍫|🚫|🗼|🐪|🍩|🗿|🔵|🍖|🔷|🔶|⛅|❄|🔳|🔲|🔽|🔼|♊|🔹|🚗|🔻|🔺|🔥|🆎|🔧|🔦|🔡|❔|🔣|🔢|🔭|🍒|🔯|🔮|🔩|🔨|🔫|🔪|🔕|🔔|🔗|🔖|🔑|❤|🔓|🔒|🔝|🔜|🔟|🍑|🔙|🔘|🔛|🔚|🔅|🚝|🚰|🔆|⛵|🔀|🔃|🚜|🔍|🃏|🔏|👊|🔉|🚟|🔋|🔊|🚞|⬇|🗽|🍚|9⃣|🗾|✏|🚘|🚳|☕|🚛|🚚|🍆|🍇|⚪|🍄|🀄|🚆|🚁|🎋|🍃|🍀|🍁|🚍|🍏|🍌|🚎|♥|🍊|⛪|⏬|🍋|⛺|🎶|🎷|🎴|🎵|🎲|🎳|🎰|⬆|🎾|🎿|🎼|🎽|🎺|🎻|🎸|🎹|🎦|🎧|⚓|🎥|🎢|🎣|🎠|🎡|🎮|🎯|🎬|🎭|🎪|🎫|🎨|🎩|™|🎒|🎓|🎐|🎑|🍼|🙅|🎇|🙇|🙆|🎂|🙀|🎀|🎁|🙍|🙌|🙏|🙎|🙉|🙈|🙋|🙊|😵|😴|😷|😶|😱|😰|😳|😲|😽|😼|😿|😾|😹|😸|😻|😺|😥|😤|😧|🏥|😡|😠|😣|😢|😭|🏯|🏬|🏭|😩|😨|😫|😪|😕|😔|😗|😖|😑|😐|😓|😒|😝|😜|😟|😞|🇯🇵|😘|😛|😚|😅|😄|⛳|😆|😁|🏃|😃|😂|😍|😌|😏|😎|😉|😈|😋|😊|🌷|🌴|🌵|🍺|🌳|🌰|🌱|✉|🌿|🌼|🌽|🌺|🌻|🌸|🌹|🌠|🌖|🌗|🌔|🌕|🌒|🌓|🌐|🌑|🌞|🌟|🌜|▪|🌚|🌛|🌘|🌙|🌆|🌇|🌄|🌅|🌂|🛀|🌀|🌁|🌎|🌏|🌌|🔎|🌊|🌋|🌈|🌉|🍶|🍷|🍴|🚶|🍲|🍳|🍰|🚲|🚽|🚼|🚿|🚾|🚹|🍻|🚻|🚺|🍦|🚤|🚧|🍥|🍢|🍣|🍠|🚢|🚭|🍯|🍬|🍭|🍪|🚨|🍨|🚪|🚕|🍗|🍔|🍕|🚑|🍓|🚓|🚒|🍞|🍟|🍜|🍝|🚙|🍛|🍘|🍙|🚅|🚄|🚇|🍅|🍂|🚀|🚃|2⃣|🍎|🚌|🚏|🍍|🚉|🚈|🍈|🍉|7⃣|✈|☎|🇫🇷|↗|📱|📰|✨|🚡|🍤|♎|⭐|🚠|🔇|⏫|📦|🈶|🈷|🈴|🈵|🈲|🈳|📢|🈺|🈸|🈹|📬|🈯|⌛|🇷🇺|👛|🈚|1⃣|🈂|📫|🈁|〽|⚾|♉|⛎|❓|🉐|🉑|🚯|⏰|✂|🚮|😦|✒|↙|⌚|🇰🇷|↩|🎱|🚊|#⃣|♌|🐖|🎤|0⃣|🚦|🔁|⬅|💴|💶|💰|💳|🔬|💲|💽|▶|ℹ|🚔|😬|💸|🚵|⭕|💻|👍|⏪|🚐|💦|🗻|🚖|💡|💠|✌|➗|💬|♣|🎆|💮|©|▫|🐊|🎄|🎅|💪|⚽|🎃|💔|❌|🎎|♒|🎏|🎌|🎍|🎊|💒|‼|🎈|◻|🎉|⛽|💞|💘|🍐|↘|☝|⬛|🏰|👔|®|♈|◀|6⃣|❇|⁉|♍|🌲|❗|💼|❎|🏦|🍸|🏧|🏤|🇩🇪|⛲|💋|🏢|💊|🏣|☀|🏠|🏡|🏮|↕|✖|😯|➡|😮|🏉|🏪|⚫|✳|🏫|🏨|🏩|🔂|🔄|♐|♠|🕤|⏩|🇮🇹|♨|◽|🕠|😙|🕢|🇪🇸|➖|📞|⚠|🌝|🏇|↪|🏄|⤵|🏂|5⃣|😀|🏀|♋|🏁|🚸|🏊|🕒|🏈|🕜|♻|🛅|㊙|🛄|🕚|⚡|🌾|⤴|🔞|✴|🚂|☺|8⃣|♦|🔌|⏳|🛁|4⃣|🇺🇸|🇬🇧|☁|🔴|✋|🇨🇳|☑|↔|🔱|🔰|🛃|➰|😇|🏆|Ⓜ|🛂|🔸|♑|🚴|🔤|◼|🔠|�|♡|★|■|😂|👌|🚗|💀|😒|🙏|👍|❤|😢|🙏|😂|♡|💓|😍|🔓|💓|😭|�|😒|❤|💨|✨|~💕|🍑|🎧|🔥|💪|👊|👏|😌|😈|'
    return emoji_str

# 除去词尾的标点
def RemoveTailPunctuation(line_word, i):
    if 0 == len(line_word[i]):
        return False
    word = unicode(line_word[i], 'utf-8')
    nLen = len(word)
    nDiff = 0
    sentence_end_flag = False
    sentence_end = [u'\'', u'\"', u':', u'؟', u'،', u'؛']
    if word[-1] in sentence_end:
        sentence_end_flag = True
    symbol_list = [u"\'", u':', u'-', u'\"', u'&', u')', u'(', u'/', u'\\', u'[',
                   u']']
    numstr = u'0123456789'
    special_str = u'.،»«„“”‘’@|؟–^*%<>ˇ'
    # special_str=special_str.decode('unicode_escape').encode("utf-8")
    for nIndex in range(nLen - 1, -1, -1):
        str = word[nIndex]
        if ((not str in symbol_list) and (not str in numstr) and (not str in special_str)):
            break
        else:
            nDiff = nDiff + 1
    line_word[i] = word[0:nLen - nDiff].encode('utf-8')

    return sentence_end_flag


# 移除词开头的引号
def RemoveHeadQuotation(line_word, i):
    if (0 == len(line_word[i])):
        return False
    word = unicode(line_word[i], 'utf-8')
    nLen = len(word)
    nDiff = 0
    symbol_list = [u"\'", u':', u'-', u'\"', u'&', u')', u'(', u'/', u'\\', u'[',
                   u']']
    numstr = u'0123456789'
    special_str = u'.،»«„“”‘’@|؟–^*%<>ˇ'
    for nIndex in range(0, nLen):
        str = word[nIndex]
        if ((not str in symbol_list) and (not str in numstr) and (not str in special_str)):
            break
        else:
            nDiff = nDiff + 1
    line_word[i] = word[nDiff:nLen].encode('utf-8')
    if 0 != nDiff:
        return True
    else:
        return False


def loadAllChars():
    #files = glob.glob("./character/*.txt") #本地
    files = glob.glob("demo_for_format/character/*.txt") #集群
    chars = set()
    for fpath in files:
        f = open(fpath)
        for line in f.readlines():
            line = line.decode("utf-8")
            if line.strip() == "":
                continue
            ch = line.strip().split("\t")[0]
            if ch == "-":
                continue
            chars.add(ch)
    return u"[" + u"".join(chars) + u"]+"
	
allchars = loadAllChars()
#allchars = u"[АДИМРФШъЬадимрÃDÇHËLÏPÓŒTXÛãdçhëlïpótxûÿсуГЗхЛПУч'Ы/щгзÈлыпяÀCGэKOSÔWÎÜàcgèkЦosôwüёВЖКОТ&Ъ.вжкоÁBFÉJÍNÑRÕVÙZÝábféjínñrõvùŸzýЯЁБЮтЕЙНфСХюЩцЭбешйнAÂEÆIÊMьQœÒUYÚaâeЧæiêmîqòuyú]+"
#allchars = u"[АДИМРФШъЬадимрÃDÇHËLÏPÓŒTXÛ\ßãdçhëlïpótxûÿсуГЗхЛПУч'Ы/щгзÈлыпяÀCÄGэKÌOSÔWÎÜàcägèkЦìosôwüёВЖКОТ&Ъ.вжкоÁBFÉJÍNÑRÕVÙZÝábféjínñrõvùŸzýЯЁБЮтЕЙНфСХюЩцЭбешйẞнAÂEÆIÊMьQœÒUÖYÚaâeЧæiêmîqòuöyú]+"
#print "allchars : " + allchars
sys.stderr.write("allchars : " + allchars + "\n")

# 按标点分句
def get_sentence_clone(line,sentence_list):
    line = line.strip()
    line = re.sub('"|”|“|', '', line)
    line = re.sub('\.', ' .\n', line)
    line = re.sub('\?', ' ?\n', line)
    line = re.sub('\!', ' !\n', line)
    line_list_one = line.split('\n')
    allchar_pattern = allchars + "|\w+"
    for item in line_list_one:
        if re.search(allchar_pattern, unicode(item)):
            sentence_list.append(item.strip())

def get_sentence(line):
    line_list_one = line.split(';')
    sentence_1 = ""
    for i in range(len(line_list_one)):
        if len(line_list_one[i].strip()) == 0:
            continue
        else:
            if i + 1 == len(line_list_one):
                sentence_1 += line_list_one[i].strip()
            else:
                sentence_1 += line_list_one[i].strip() + ' ; '

    line_list = sentence_1.split(',')
    sentence = ""
    for i in range(len(line_list)):
        if len(line_list[i].strip()) == 0:
            continue
        else:
            if i + 1 == len(line_list):
                sentence += line_list[i].strip()
            else:
                sentence += line_list[i].strip() + ' , '
    
    word_list = sentence.split(' ')
    str_temp = ''
    for word in word_list:
        if len(word) == 0:
            continue
        if word[0]=='\'':
            word = word[1:]
        if word[len(word)-1] == '\'':
            word = word[0:-1]
        #if word in check_list:
        #   continue
        
        #if len(word)>1 and word not in check_list_word: #or word != 'NUM' or word != 'USER':
        #   continue    
        if len(word) == 1 and word == '-':
            continue
        str_temp += word+' '        
                    
    return str_temp

invalid_alone_tags = set(["'", '"'])
def modify_word(word):
    chs = set(word)	
    if len(chs) == 1 and chs <= invalid_alone_tags:
        return ""
    while word[0] in invalid_alone_tags:
        word = word[1:]
    while word[-1] in invalid_alone_tags:
        word = word[:-1]
    return word

# remove continuous same char
cont_chars = set(['-'])
def modify_sent(sent):
    new_sent = ""
    lastch = ""
    for ch in cont_chars:
        for i in range(len(sent)):
            if sent[i] == ch and ch == lastch:
                continue
            new_sent += sent[i]
            lastch = sent[i]
    return new_sent


for line in sys.stdin:
    try:
        oriline = line.strip()
        infos = oriline.split("\t")
	
        if len(infos) != 2:
            continue

        lang = infos[0].strip()
        sent = infos[1].strip()
        
        words = sent.split(' ')
        str_sentence = ''

        for word in words:
            word = word.strip()
            word = modify_word(word)
            if len(word)==0:
                continue
            elif word[0] == '#':
                continue
            else:
                str_sentence += word + ' '
        str_sentence = re.sub(',','#',str_sentence)

        # remove urls
        str_sentence = re.sub("(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", " ", str_sentence)
        
        # remove "<br>"
        str_sentence = re.sub("<br>", "", str_sentence)

        # filter characters
        pattern = allchars + "|\w+|\.|\?|@\w+|\!|#|;|\s+|\'|-|\d+"
        str_list = re.findall(pattern, unicode(str_sentence))


        # maintain @USER
        str_sentence = ''
        allchar_pattern = allchars + "|\w+|@\w+"
        for str_word in str_list:
            str_word = str_word.encode('utf-8')
            if len(str_sentence)==0 and (re.match(allchar_pattern, unicode(str_word))):
                str_sentence += str_word.strip()+' '
            elif len(str_sentence)>0 and str_word != '\'' and str_word != '-':
                str_sentence += str_word.strip()+' '
            elif str_word == '\'' or str_word == '-':
                str_sentence = str_sentence.strip()
                str_sentence += str_word.strip()
        word_list = str_sentence.split(' ')
        #for i in range(len(word_list)):
        #    RemoveTailPunctuation(word_list, i)
        #for i in range(len(word_list)):
        #    RemoveHeadQuotation(word_list, i)
        str_sentence = ""
        for word_line in word_list:
            if len(word_line) > 0 and word_line != ' ':
                str_sentence += word_line + ' '

        sentence = str_sentence
        if len(sentence)==0:
            continue
        sentence = re.sub('_','',sentence)
        sentence = re.sub(get_emoji(),'',sentence)
        sentence = re.sub('\s+', ' ', sentence)
        sentence = re.sub(r'[,]+', ',', sentence)
        sentence = re.sub(r'[#]+', ',', sentence)
        sentence = re.sub('\s+', ' ', sentence)
        sentence_list=[]
        get_sentence_clone(sentence,sentence_list)
        new_sent = " ".join(sentence_list)

        newtext = get_sentence(new_sent)
        newtext = modify_sent(newtext)
        print lang + "\t" + newtext
    except Exception, e:
        sys.stderr.write(str(e))

