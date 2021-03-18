import sys
import re
import pathlib
from src import utils
import os
from src.config import *
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
def searching(query_string):
    vocab = utils.get_vocabulary()
    citations = utils.get_citations()
    terms = []
    terms.extend(re.split('[^\w\']', query_string))
    terms = [word.lower() for word in terms]
    terms = [sno.stem(re.sub('\'$', '', re.sub('^\'', '', word))) for word in terms if word != '']
    allkeys = []
    diction = {}

    for x in terms:
        if x in vocab:
            if os.path.exists(("data/indexes/inverted_index_" + x + ".pbz2")):
                index = utils.load_index("data/indexes/inverted_index_" + x)
            else:
                index = utils.load_index(filename="data/indexes/inverted_index_" + x[0])
            keys = index[x]["doc_ids"].keys()
            for i in keys:
                if i not in diction.keys():
                    diction[i] = index[x]["doc_ids"][i]
                else:
                    temp = diction[i]
                    temp += index[x]["doc_ids"][i]
                    diction[i] = temp
            allkeys += keys

    def sorting_citations(n):
        return citations[n]

    def sorting_termcount(n):
        return diction[n]

    allkeys = list(set(allkeys))
    allkeys.sort(key=lambda j: (sorting_termcount(j), sorting_citations(j)), reverse=True)

    return allkeys
