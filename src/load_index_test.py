from src import utils
import time
import os
from src.config import *
from tqdm import tqdm

if __name__=="__main__":
    vocab = utils.get_vocabulary()          # loads vocabulary present in system
    citations = utils.get_citations()       # loads citation counts for doc_ids
    while True:
        print("Enter a word to search the index for:")
        x = input()

        if x != "":
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
                print(index[x]["doc_frequency"])
                for k in list(index[x]["doc_ids"])[:10]:
                    print(k, citations[k])
            else:
                print("Sorry, this word is not in the index. Try another.")