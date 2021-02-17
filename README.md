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
> export FLASK_APP=app.py
> flask run
# Then go to http://127.0.0.1:5000/ in your browser
```


## Meeting Notes

| Meeting     | Description |
| ----------- | ----------- |
| 20 Jan      | Set out initial plan, each team member will look into their respective areas. These include fron-end, back-end (database, hosting), main information retrieval algorithm, and data collection. |
| 20 Jan      | TBD        |
