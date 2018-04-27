import sys


def lcs_len(s1,s2):
    m=[[0 for i in range(len(s2)+1)]  for j in range(len(s1)+1)]
    mmax=0
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i]==s2[j]:
                m[i+1][j+1]=m[i][j]+1
                if m[i+1][j+1]>mmax:
                    mmax=m[i+1][j+1]
    return mmax


input = sys.argv[1]
input_file = open(input, "r")
input_list = input_file.readlines()

for i in xrange(len(input_list)):
    j = i - 1
    str_i = input_list[i]
    if str_i[0] == '#':
        continue
    
    while j > 0 and input_list[j][0] != '#':
        if input_list[j] == "\n":
            j -= 1
            continue

        sys.stderr.write(str(i) + "\t" +str(j) + "\t")
        str_j = input_list[j]
        ll =  lcs_len(str_i, str_j)
        appro = float(ll) / min(len(str_i), len(str_j))
        sys.stderr.write(str(appro) + "\n")
        if appro > 0.6:
            short = i if len(str_i) < len(str_j) else j
            input_list[short] = "\n"

        j -= 1

for i in input_list:
    print i,


