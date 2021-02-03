import os
import json

def get_index_from_json(filename):
    papers_index = dict()
    with open(filename, "r") as f:
        j = json.load(f)                                                                    # array of paper dictionaries
        for p in j["papers"]:
            paper = dict()

            # remove newlines and ignore unicode characters
            total_content = p["abstract"].replace('\n', ' ').encode('ascii', 'ignore') + b' ' + p["content"].replace('\n', ' ').encode('ascii', 'ignore')

            # get other metadata
            paper["title"] = p["title"]                 # title
            paper["authors"] = p["authors"]             # authors
            d = ""
            for v in p["versions"]:
                if v["version"] == "v1":
                    d = v["created"]
            paper["date"] = d                           # date submitted (e.g. [Day], [d] [Mon] [y] HH:MM:ss [Zone])
            paper["categories"] = p["categories"]       # categories
            paper["words"] = str(total_content)         # content of paper

            papers_index[p["id"]] = paper
    return papers_index

def main():
    papers_index = get_index_from_json("../arxiv_sampled.json")
    print(list(papers_index.keys()))

if __name__=="__main__":
    main()