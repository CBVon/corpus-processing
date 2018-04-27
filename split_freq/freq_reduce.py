import sys


last_text = ""
last_lang = ""
last_sf = 0
for line in sys.stdin:
	line = line.strip()
	infos = line.split("\t")
	if len(infos) != 3:
		continue
	lang = infos[0]
	text = infos[1]
	sf = int(infos[2])

	if (last_lang != "" and lang != last_lang) or (last_text != "" and text != last_text):
		print last_lang + "\t" + last_text + "\t" + str(last_sf)
		last_lang = lang
		last_text = text
		last_sf = sf
		continue

	last_lang = lang
	last_text = text
	last_sf += sf

print last_lang + "\t" + last_text + "\t" + str(last_sf)
