import bz2
import _pickle as pickle
import os
from tqdm import tqdm

def load_index(filename="inverted_index"):
    """ Load saved index. """
    index = dict()
    for i in tqdm(os.listdir("indexes"), ascii=True, desc="Processing files into index"):
        with bz2.BZ2File("indexes/" + i, "rb") as f:
            new = pickle.load(f)
            for k in list(new.keys()):
                if k not in index:
                    # if we have a new term initialise index with info
                    index[k] = new[k]
                else:
                    # else merge the data
                    index[k]["doc_frequency"] += new[k]["doc_frequency"]
                    for pid in list(new[k]["doc_positions"].keys()):
                        index[k]["doc_positions"][pid] = new[k]["doc_positions"][pid]
    return index

def save_index(index, filename="inverted_index"):
    """ Save index object in compressed file. """
    with bz2.BZ2File(filename + ".pbz2", "wb") as f:
        pickle.dump(index, f)