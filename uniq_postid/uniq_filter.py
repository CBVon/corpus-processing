import sys


last_postid = ""
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

	if last_postid != "" and postid != last_postid:
		print 'unk\t' + last_text
	last_postid = postid
	last_text = text

print "unk\t" + last_text
