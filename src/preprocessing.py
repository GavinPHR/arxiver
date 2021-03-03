from config import *
import re
from stemming.porter2 import stem

def tokenise(terms):
    # create list of words to return
    words = []
    # split input on non alphanumeric characters and convert to lowercase
    words.extend(re.split('[^\w\']', terms.lower()))

    # stem words and/or remove empty strings, convert 'term' to term
    if STEMMING:
        words = [sno.stem(re.sub('\'$', '', re.sub('^\'', '', word))) for word in words if word != '' and not any(char.isdigit() for char in word) and word[0] != '\\']
    else:
        words = [re.sub('\'$', '', re.sub('^\'', '', word)) for word in words if word != '' and not any(char.isdigit() for char in word) and word[0] != '\\']

    return words

def stop(words):
    # remove stop words from list of words
    return [word for word in words if word not in STOP_WORDS]