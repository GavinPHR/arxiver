import sys
import re

# the file which contains the index
indexFile = "index.txt"
alphabet = {}


def get_docs(term):
    # given a term return the docID its in
    list1 = alphabet[term]
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
    terms = []
    terms.extend(re.split('[^\w\']', query_string))
    terms = [stem(re.sub('\'$', '', re.sub('^\'', '', word))) for word in terms if word != '']
    out = ""

    if terms.count("AND") == 1:
        term1_docs = get_docs(terms[0].lower())
        term2_docs = get_docs(terms[2].lower())
        out = search_and(term1_docs, term2_docs)

    if terms.count("OR") == 1:
        term1_docs = get_docs(terms[0].lower())
        term2_docs = get_docs(terms[2].lower())
        out = search_or(term1_docs, term2_docs)

    if len(terms) == 1:
        out = get_docs(terms[0].lower())

    return out
