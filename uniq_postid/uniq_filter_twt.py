import sys


#langs = ["id", "es", "ru", "pt", "fr", "en", "de"]
#langs = ["id", "es", "ru", "pt", "fr", "de"]
#langs = ["it", "tl"]
langs = ["id", "es", "ru", "pt", "fr", "de", "it", "tl"] #20180531

last_postid = ""
last_lang = ""
last_text = ""
for line in sys.stdin:
	line = line.strip()
	line_items = line.split("\t")
	if len(line_items) != 6:
		continue

	postid = line_items[0]
	#userid = line_items[2]
	#username = line_items[3]
	text = line_items[4]
	lang = line_items[5]
	if lang == "in":
		lang = "id"
	if lang not in langs:
		continue

	if last_postid != "" and postid != last_postid:
		print last_lang + '\t' + last_text
	last_postid = postid
	last_lang = lang
	last_text = text

print last_lang + '\t' + last_text


