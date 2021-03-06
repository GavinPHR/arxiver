from src import utils
import time
import os
from src.config import *

if __name__=="__main__":
    while True:
        print("Enter a word to search the index for:")
        x = input()

        if x != "":
            start_time = time.time()
            if os.path.exists(("indexes/inverted_index_" + x + ".pbz2")):
                index = utils.load_index("indexes/inverted_index_" + x)
                loaded = x
            else:
                index = utils.load_index(filename="indexes/inverted_index_" + x[0])
                loaded = x[0]
            end_time = time.time()
            print(("Took {} seconds to load index " + loaded).format(end_time-start_time))

            try:
                print(index[x]["doc_frequency"])
            except KeyError:
                print("Sorry, this word is not in the index. Try another.")