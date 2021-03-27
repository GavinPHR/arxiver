import sys
import re
import pathlib
from src import utils
import os
from src.config import *
from app import vocab, citations
from collections import Counter
from math import log2
# the file which contains the index
indexFile = str(pathlib.Path(__file__).parent.absolute()) + "/index.txt"
alphabet = {}


def get_docs(term):
    # given a term return the docID its in
    list1 = alphabet.get(term, [])
    ids = []
    for (paper_id, pos) in list1[1:]:
        ids.append(paper_id)
    return ids


def search_or(list1, list2):
    out_list = list1 + list2
    out_list = list(set(out_list))
    out_list.sort()
    return out_list


def search_and(list1, list2):
    set1 = set(list1)
    set2 = set(list2)
    out = list(set1.intersection(set2))
    out.sort()
    return out


# reads the index file and loads it to memory
def load_index():
    f = open(indexFile, "r")
    for line in f:
        line = line.strip("\n")
        if re.search("^\S+:", line):
            x = re.split("\:", line)
            # txt = re.search( "^\S+",line).group().strip(":")
            # dfz = re.search("\d+",line).group()
            txt = x[0]
            dfz = x[1]
            alphabet[txt] = [("df", dfz)]
            prev = txt
        elif re.search("^:", line):
            x = re.split("\:", line)
            txt = x[0]
            dfz = x[1]
            alphabet[txt] = [("df", dfz)]
            prev = txt
        elif re.search("^\t(\S+):", line):
            iD = re.search("^\t(\S+)", line).group().strip("\t").strip(":")
            poslist = re.findall("(\d+)", line)
            list3 = alphabet.get(prev)
            list3.append((iD, poslist[1:]))

    f.close()


# takes in the query as a string and then returns the paper IDs
def searching(query_string, length):
    terms = []
    terms.extend(re.split('[^\w\']', query_string))
    terms = [word.lower() for word in terms]
    terms = [sno.stem(re.sub('\'$', '', re.sub('^\'', '', word))) for word in terms if word != '']
    terms = [word for word in terms if word in vocab]
    docs = set()
    freq = Counter()
    appearance = Counter()

    for x in terms:
        if os.path.exists((INDEX_PATH + "/inverted_index_" + x + ".pbz2")):
            index = utils.load_index(INDEX_PATH + "/inverted_index_" + x)
        else:
            index = utils.load_index(INDEX_PATH + "/inverted_index_" + x[0])
        keys = index[x]["doc_ids"].keys()
        for i in keys:
            freq[i] += int(log2(index[x]["doc_ids"][i]))
            appearance[i] += 1
        docs.update(keys)
    res, tmp = [], []
    ranked = sorted(docs, key=lambda x: appearance[x], reverse=True)[:length]
    ranked.append(None) # boundary
    prev = None
    for doc in ranked:
        if appearance[doc] != prev:
            prev = appearance[doc]
            tmp.sort(key=lambda x: citations[x], reverse=True)
            res.extend(tmp)
            tmp = []
        if doc is not None:
            tmp.append(doc)
    return res
