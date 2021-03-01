import bz2
import _pickle as pickle
import os
from tqdm import tqdm

def load_index(filename="inverted_index"):
    """ Load saved index. """
    with bz2.BZ2File(filename + ".pbz2", "rb") as f:
        index = pickle.load(f)
    return index

def save_index(index, filename="inverted_index"):
    """ Save index object in compressed file. """
    with bz2.BZ2File(filename + ".pbz2", "wb") as f:
        pickle.dump(index, f)