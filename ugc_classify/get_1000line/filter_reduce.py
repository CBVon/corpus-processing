import sys
import random
#python filter_reduce line_num

line_num = int(sys.argv[1])
for line in sys.stdin:
    ri = random.randint(1, line_num)
    if ri <= 1000:
        print line.strip()


