# global vars
STEMMING = True
STOPPING = False
JSON_PATH = "../arxiv_sampled.json"
STOP_PATH = "../englishST.txt"

def get_stop_words():
    lines = open(STOP_PATH, 'r', encoding='utf-8-sig').readlines()

    # create list of words to return
    words = []
    for line in lines:
        words.extend(re.split('[^\w\']', line))

    # stem words and/or remove empty strings, convert 'term' to term
    if STEMMING:
        stops = set([stem(re.sub('\'$', '', re.sub('^\'', '', word))) for word in words if word != ''])
        return stops
    
    return set([re.sub('\'$', '', re.sub('^\'', '', word)) for word in words if word != ''])

STOP_WORDS = get_stop_words() + "" if STOPPING else set("")