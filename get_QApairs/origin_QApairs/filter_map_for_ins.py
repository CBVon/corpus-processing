import sys
import json


reload(sys)
sys.setdefaultencoding("utf-8")

for line in sys.stdin:
    #sys.stderr.write(line)
    
    d_line = {}

    try:
        d_line = json.loads(line.decode("utf-8").strip())
    except Exception, err:
        sys.stderr.write(line)
        sys.stderr.write(str(err) + "\n")
        continue
    
    Q = ""
    A = ""
    if "graphql" in d_line:
        if "shortcode_media" in d_line["graphql"]:
            if "edge_media_to_caption" in d_line["graphql"]["shortcode_media"]:
                if "edges" in d_line["graphql"]["shortcode_media"]["edge_media_to_caption"]:
                    if len(d_line["graphql"]["shortcode_media"]["edge_media_to_caption"]["edges"]) == 1 and "node" in d_line["graphql"]["shortcode_media"]["edge_media_to_caption"]["edges"][0]:
                        if "text" in d_line["graphql"]["shortcode_media"]["edge_media_to_caption"]["edges"][0]["node"]:
                            Q = d_line["graphql"]["shortcode_media"]["edge_media_to_caption"]["edges"][0]["node"]["text"].replace("\n", ". ").replace("\t", " ").encode("utf-8").strip()
            
            if Q != "" and "edge_media_to_comment" in d_line["graphql"]["shortcode_media"]:
                if "edges" in d_line["graphql"]["shortcode_media"]["edge_media_to_comment"]:
                    if len(d_line["graphql"]["shortcode_media"]["edge_media_to_comment"]["edges"]) > 0:
                        for comment_d in d_line["graphql"]["shortcode_media"]["edge_media_to_comment"]["edges"]:
                            if "node" in comment_d:
                                if "text" in comment_d["node"]:
                                    A = comment_d["node"]["text"].replace("\n", ". ").replace("\t", " ").encode("utf-8").strip()
                                    if A != "":
                                        print Q + "\t" + A
                    

