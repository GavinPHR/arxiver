import utils
import time
import os
from config import *
from tqdm import tqdm

if __name__=="__main__":
    vocab = utils.get_vocabulary()          # loads vocabulary present in system
    citations = utils.get_citations()       # loads citation counts for doc_ids
    while True:
        print("Enter a word to search the index for:")
        x = input()

        if x in vocab:
            start_time = time.time()
            if os.path.exists(("indexes/inverted_index_" + x + ".pbz2")):
                index = utils.load_index("indexes/inverted_index_" + x)
                loaded = x
            else:
                index = utils.load_index(filename="indexes/inverted_index_" + x[0])
                loaded = x[0]
            end_time = time.time()
            print(("Took {} seconds to load index " + loaded).format(end_time-start_time))
            print(index[x]["doc_frequency"])                        # print number of docs term is in
            for k in list(index[x]["doc_ids"].keys())[:10]:
                print(k, index[x]["doc_ids"][k], citations[k])      # print top 10 docs for term, how many times term in doc, and citations of doc
        else:
            print("Sorry, this word is not in the index. Try another.")