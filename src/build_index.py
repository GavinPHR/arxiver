import os
import json
import re
from src.config import *
from src import preprocessing, utils
import time
import numpy as np
from tqdm import tqdm

CITATION_COUNTS = dict()

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
    paper["citations"] = p["timescited"]

    return paper, paperID

def build_papers_index(filename, save=False):
    paper_index = dict()
    with open(filename, "rb") as f:
        papers_as_json = f.readlines()          # since one paper in json per line

        for p in papers_as_json:
            paper, paperID = get_paper_from_json(p)
            paper_index[paperID] = paper
            CITATION_COUNTS[paperID] = paper["citations"]

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

def sort_indexes():
    for l in tqdm(os.listdir(INDEX_PATH), ascii=True, desc="Sorting indexes"):
        index = utils.load_index("indexes/" + l.split(".")[0])
        index = {k: v for k, v in reversed(sorted(index.items(), key=lambda item: item[1]["doc_frequency"]))}

        for term in index.keys():
            index[term]["doc_ids"] = {k: v for k, v in reversed(sorted(index[term]["doc_ids"].items(), key=lambda item: item[1]))}

        utils.save_index(index, filename="indexes/" + l.split(".")[0])

def remove_single_docs():
    for l in tqdm(os.listdir(INDEX_PATH), ascii=True, desc="Removing terms with single doc_frequency"):
        index = utils.load_index("indexes/" + l.split(".")[0])
        for term in list(index.keys()):
            for doc_id in list(index[term]["doc_ids"].keys()):
                if index[term]["doc_ids"][doc_id] <= 1:
                    index[term]["doc_ids"].pop(doc_id)
                    index[term]["doc_frequency"] -= 1

            if index[term]["doc_frequency"] < 1:
                index.pop(term)
        utils.save_index(index, filename="indexes/" + l.split(".")[0])

def remove_frequent_terms(frequency=100):
    for l in tqdm(os.listdir(INDEX_PATH), ascii=True, desc="Giving most frequent terms their own index"):
        index = utils.load_index("indexes/" + l.split(".")[0])
        for term in list(index.keys()):
            if index[term]["doc_frequency"] > frequency:
                new = {term: index[term]}
                utils.save_index(new, "indexes/inverted_index_" + term)
                index.pop(term)
        utils.save_index(index, filename="indexes/" + l.split(".")[0])

def main():
    try:
        os.makedirs("indexes")
    except:
        pass
    for filename in os.listdir(ARXIV_PATH):
        papers_index = build_papers_index(ARXIV_PATH + filename)
        inverted_index = build_inverted_index(papers_index, debug=False, desc=filename)
        split_and_save(inverted_index)
    sort_indexes()
    remove_single_docs()        # 2.25GB before, 1.19GB after
    remove_frequent_terms()
    utils.save_index(CITATION_COUNTS, filename="citations")

if __name__=="__main__":
    main()