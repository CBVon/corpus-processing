import sys


last_sent = ""
last_sf = 0
for i in sys.stdin:
    line = i.strip()
    sent = line.split('\t')[0]
    sf = int(line.split('\t')[1])

    if sent == last_sent:
        last_sf += sf
    elif sent != last_sent:
        print last_sent + "\t" + str(last_sf)

        last_sent = sent
        last_sf = sf

print last_sent + "\t" + str(last_sf)
