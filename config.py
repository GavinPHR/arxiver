import nltk
import string

# global vars
STEMMING = True
STOPPING = True
ARXIV_PATH = "W:/dev/arxiv_archive/"
INDEX_PATH = "indexes/"
JSON_PATH = ARXIV_PATH + "papersaa.txt"
STOP_PATH = "englishST.txt"
VOCABULARY_PATH = "vocabulary.pbz2"

ALPHABET = list(string.ascii_lowercase)

if STEMMING:
    porter = nltk.stem.porter.PorterStemmer()
    sno = nltk.stem.snowball.SnowballStemmer("english")

def get_stop_words():
    import re
    lines = open(STOP_PATH, "r", encoding="utf-8-sig").readlines()

    # create list of words to return
    words = []
    for line in lines:
        words.extend(re.split("[^\w\']", line))

    # stem words and/or remove empty strings, convert "term" to term
    if STEMMING:
        stops = set([sno.stem(re.sub('\'$', '', re.sub('^\'', '', word))) for word in words])
        return stops
    
    return set([re.sub('\'$', '', re.sub('^\'', '', word)) for word in words])

STOP_WORDS = get_stop_words()