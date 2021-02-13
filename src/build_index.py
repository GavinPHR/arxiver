import os
import json
import re
import preprocessing
import time
import bz2
import _pickle as pickle
import numpy as np
from config import *

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
            paper["content"] = str(total_content)       # content of paper

            papers_index[p["id"]] = paper
    return papers_index

def build_index(papers_index, debug=False):
    """
        Build index of the form:
            { term: { doc_frequency,
                      doc_positions: 
                            { docID: [pos1, pos2, ...],
                              docID: [pos1, pos2, ...]}
                    }
            }
    """
    start_time = time.time()
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
    for sw in STOP_WORDS:
        index.pop(sw)
    index.pop("")
    end_time = time.time()

    if debug:
        print(len(list(index.keys())))
        print(index["test"])
        print(end_time - start_time)

    return index

def save(index, filename="inverted_index"):
        """ Save current replay buffer. """
        with bz2.BZ2File(filename + ".pbz2", "wb") as f:
            pickle.dump(index, f)

def main():
    papers_index = get_index_from_json("../arxiv_sampled.json")
    # print(list(papers_index.keys()))
    inverted_index = build_index(papers_index, debug=True)
    save(inverted_index)

if __name__=="__main__":
    main()