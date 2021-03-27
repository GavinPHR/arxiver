# arxiver

The search file contains two functions one which loads the index from the text file and a second that does the searching.

The searching function takes the query as an input and then returns the papers IDs. It currently only does simple boolean search with AND and OR.

Practical Group Coursework for Text Technologies for Data Science

## Initial Setup
```bash
# Clone this repo
> git clone https://github.com/GavinPHR/arxiver.git
> cd arxiver
# Make/activate a virtual environment
> python3 -m venv venv
> source venv/bin/activate
# Install reqruied packages
> pip install -r requirements.txt
```

## Start Web Server
```bash
> python3 app.py
# Then go to http://127.0.0.1:5000/ in your browser
```


## Meeting Notes

## Retrieval

To construct the index, simply run
```bash
> python -B build_index.py
```
The index is a dictionary with a key for each term. At each key is a dictionary with two items:
- doc_frequency (the number of documents the term appears in)
- doc_positions (a dictionary with paper IDs for keys, and a list with the positions the term appears in docID)

For example, `index["test"]["doc_frequency"]` will return the number of documents the word "test" appears in. And `index["test"]["doc_ids"]` will return a dictionary i.e. {"1011.9011": num_occurrences, ...}.

The index will be automatically saved, but an index can be loaded in other parts of the code by importing `utils`, and using the function `utils.load_index(INDEX_PATH)`. This will load the index in the exact format it was constructed in using pickle.

The stemmer used was a [Snowball stemmer](https://www.nltk.org/_modules/nltk/stem/snowball.html).

## How to get and work with full indexes

The full indexes, vocabulary and citation counts are available at: https://drive.google.com/file/d/1WvnlhwG5GZijQBOcXRighzMOIOHQE5wQ/view?usp=sharing

You will require about 1GB to decompress all the data. Simply extract the archive such that each of vocabulary.pbz2, citations.pbz2, and the indexes folder are in src. Then, for an example on how to load and search this data efficiently, check [load_index_test.py](https://github.com/GavinPHR/arxiver/blob/main/src/load_index_test.py).

| Meeting     | Description |
| ----------- | ----------- |
| 20 Jan      | Set out initial plan, each team member will look into their respective areas. These include fron-end, back-end (database, hosting), main information retrieval algorithm, and data collection. |
| 20 Jan      | Andrew and Ben will look into different aspects of the main algorithm, Jie will continue with the data, Gavin will start implement some web stuff       |
| 03 Feb      | Andrew and Ben will get the coursework code adapted to this project, Jie will continue with data cleaning, Gavin will implement the rest of the web functionalities. In the next meeting, we should have individual parts almost ready and be able to fit them together.        |
| 10 Feb      | Same as last meeting.   |
| 17 Feb      | 1. There is currently no way to rank the papers (besides according to dates), Jie will be working on getting citation counts so it would be easier to rank. For now, Gavin will assign some random citation counts to do some experiments with ranking. 2. As discussed last week, there is indeed no need to host the full dataset on the server. We should be only hosting the index, and for every paper, we will need to host its title, authors, abstract, link to pdf. 3. The queries seem to be not stemmed, which results in keyerros in the alphabet, and the search does not return any results. Andrew will try to fix that. 4. With 1220000 papers, the currently time for building the index is prohibitively long. Maybe Ben can look into methods where stemming is not required (if stemming is indeed taking the most time)? |
| 24 Feb      | Not Recorded |
| 03 Mar      | Some memory issues, trying either to remove docs with 1 word occurance, or save an index for each high-frequency word. Jie will get the citations. More front-end and ranking should be done before next week. |
