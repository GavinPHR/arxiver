# arxiver

The search file contains two functions one which loads the index from the text file and a second that does the searching.

The searching function takes the query as an input and then returns the papers IDs. It currently only does simple boolean search with AND and OR.

Practical Group Coursework for Text Technologies for Data Science


## Retrieval

To construct the index, simply run
```bash
> python -B build_index.py
```
The index is a dictionary with a key for each term. At each key is a dictionary with two items:
- doc_frequency (the number of documents the term appears in)
- doc_positions (a dictionary with paper IDs for keys, and a list with the positions the term appears in docID)

Dictionaries are used since I think they are the fastest data structure that is appropriate for this sort of data task, but there may be better options I am not aware of.

The index will be automatically saved, but can be loaded in other parts of the code by importing `utils`, and using the function `utils.load_index()`. This will load the index in the exact format it is constructed in using pickle.

Stopping and stemming can be enabled/disabled in `config.py`. The stemmer is a [Snowball stemmer] (https://www.nltk.org/_modules/nltk/stem/snowball.html). This is faster than the alternative Porter stemmer. To switch between the two, just change every mention of `sno` to `porter` in `preprocessing.py` and `config.py`, but there isn't much point as the Snowball stemmer is far quicker than the Porter stemmer.


| Meeting     | Description |
| ----------- | ----------- |
| 20 Jan      | Set out initial plan, each team member will look into their respective areas. These include fron-end, back-end (database, hosting), main information retrieval algorithm, and data collection. |
| 20 Jan      | TBD        |
