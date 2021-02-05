import os
import json
import re
import config
import preprocessing

def get_index_from_json(filename):
    papers_index = dict()
    with open(filename, "r") as f:
        j = json.load(f)                                # list of paper json objects (i.e. dictionaries)
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
                    break
            paper["date"] = d                           # date submitted (e.g. [Day], [d] [Mon] [y] HH:MM:ss [Zone])
            paper["categories"] = p["categories"]       # categories
            paper["content"] = str(total_content)         # content of paper

            papers_index[p["id"]] = paper
    return papers_index

def build_index(papers_index):
    """
        Build index of the form:
            term: doc_frequency
                  doc_positions:
                        docID: pos1, pos2, ...
                        docID: pos1, pos2, ...
    """
    unique_terms = set()
    for paperID in list(papers_index.keys()):
        content = papers_index[paperID]["content"]
        content = preprocessing.tokenise(content)
        unique_terms |= set(content)
    
    index = dict()
    
    for term in sorted(unique_terms):
        term_info = {"doc_frequency": 0,
                     "doc_positions": dict()
                    }
        index[term] = term_info
    
    for paperID in list(papers_index.keys()):
        content = papers_index[paperID]["content"]
        content = preprocessing.tokenise(content)

        terms = set(content)
        for t in terms:
            index[t]["doc_frequency"] += 1

        for i, word in enumerate(content):
            try:
                index[word]["doc_positions"][paperID].append(i)
            except:
                index[word]["doc_positions"][paperID] = []
                index[word]["doc_positions"][paperID].append(i)
    index.pop("")
    print(index["test"])
    print(list(index.keys())[10000:10010])
    print(len(list(index.keys())))

    return index

def main():
    papers_index = get_index_from_json("../arxiv_sampled.json")
    print(list(papers_index.keys()))
    build_index(papers_index)

if __name__=="__main__":
    main()