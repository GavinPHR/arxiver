import nltk

# global vars
STEMMING = True
STOPPING = True
JSON_PATH = "../arxiv_sampled.json"
STOP_PATH = "../englishST.txt"

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

STOP_WORDS = get_stop_words() if STOPPING else set("")