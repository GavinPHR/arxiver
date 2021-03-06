import bz2
import _pickle as pickle
import os
from tqdm import tqdm
from src.config import *

def load_index(filename="inverted_index"):
    """ Load saved index. """
    with bz2.BZ2File(filename + ".pbz2", "rb") as f:
        index = pickle.load(f)
    return index

def save_index(index, filename="inverted_index"):
    """ Save index object in compressed file. """
    with bz2.BZ2File(filename + ".pbz2", "wb") as f:
        pickle.dump(index, f)

def get_vocabulary():
    try:
        vocab = load_index(VOCABULARY_PATH.split('.')[0])
        return vocab
    except:
        vocab = []
        for l in tqdm(os.listdir(INDEX_PATH), ascii=True, desc="Getting vocabulary"):
            try:
                index = load_index("indexes/" + l.split(".")[0])
                vocab.extend(list(index.keys()))
            except:
                continue
        save_index(vocab, filename=VOCABULARY_PATH.split('.')[0])
    return set(vocab)