import os
import json
import re
import preprocessing
import time
import numpy as np
import utils
from config import *
from tqdm import tqdm
import numpy as np

def get_paper_from_json(json_string):
    p = json.loads(json_string)                 # load the paper as a json object
    
    paper = dict()

    paperID = p["id"]

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

    return paper, paperID

def build_papers_index(filename, save=False):
    paper_index = dict()
    with open(filename, "rb") as f:
        papers_as_json = f.readlines()          # since one paper in json per line

        for p in papers_as_json:
            paper, paperID = get_paper_from_json(p)
            paper_index[paperID] = paper

        # save papers index to compressed file
        if save:
            utils.save_index(paper_index, filename="papers_index")
    
    return paper_index

def build_inverted_index(papers_index, debug=False, desc=""):
    """
        Build index of the form:
            { term: { doc_frequency,
                    #   doc_positions: 
                    #         { docID: term_count,
                    #           docID: term_count }
                    }
            }
    """
    index = dict()

    # loop through the papers and update the index
    for paperID in tqdm(list(papers_index.keys()), ascii=True, desc="Building index from " + desc):
        content = papers_index[paperID]["content"]
        content = preprocessing.tokenise(content)

        # get set of unique terms for doc_frequency
        unique_terms = set(content)

        for word in unique_terms:
            if word not in index:
                index[word] = {
                               "doc_frequency": 0,
                               "doc_ids": dict()
                              }
            index[word]["doc_frequency"] += 1
            index[word]["doc_ids"][paperID] = 0

        for word in content:
            index[word]["doc_ids"][paperID] += 1

    # pop all the stop words from the index
    if STOPPING:
        for sw in STOP_WORDS:
            try:
                index.pop(sw)
            except KeyError:
                pass
    else:
        try:
            index.pop("")
        except KeyError:
            pass
    # end_time = time.time()

    # if debug flag set, print some information about the data
    if debug:
        # print(STOP_WORDS)
        print(len(list(index.keys())))
        print(index["test"])
        # print(len(list(index["test"]["doc_positions"].keys())))
        try:
            print(index[""])
        except:
            pass
        # print("Took {} seconds to build.".format(round(end_time - start_time, 2)))
    return index

def split_and_save(index):
    for l in tqdm(ALPHABET, ascii=True, desc="Processing letters"):
        terms = [i for i in index.keys() if i.startswith(l)]
        try:
            tmp = utils.load_index(filename="indexes/inverted_index_" + l)
        except FileNotFoundError:
            tmp = dict()
        for term in terms:
            if term not in tmp:
                # if we have a new term initialise index with info
                tmp[term] = index[term]
            else:
                # else merge the data
                tmp[term]["doc_frequency"] += index[term]["doc_frequency"]
                for pid in list(index[term]["doc_ids"].keys()):
                    tmp[term]["doc_ids"][pid] = index[term]["doc_ids"][pid]
        utils.save_index(tmp, filename="indexes/inverted_index_" + l)

def main():
    try:
        os.makedirs("indexes")
    except:
        pass
    for filename in os.listdir("W:/dev/arxiv_archive/"):
        papers_index = build_papers_index("W:/dev/arxiv_archive/" + filename)
        inverted_index = build_inverted_index(papers_index, debug=False, desc=filename)
        split_and_save(inverted_index)
    # print(len(list(papers_index.keys())))
    # indices = np.random.choice(range(len(list(papers_index.keys()))), size=100)
    # print(list(papers_index.keys())[indices])

if __name__=="__main__":
    main()