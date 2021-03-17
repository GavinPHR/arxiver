from termcolor import colored

"""
dict_keys(['id', 'submitter', 'authors', 'title', 'comments', 
'journal-ref', 'doi', 'report-no', 'categories', 'license', 
'abstract', 'versions', 'update_date', 'authors_parsed', 'content'])
"""
import subprocess
subprocess.run(["mkdir", "/home/apps/data"])
subprocess.run(["sh", "./prep.sh"])

import json
with open('arxiv_sampled.json', 'r') as f:
    example = json.loads(f.read())
id2file = dict()
for paper in example['papers']:
    id2file[paper['id']] = paper
print(colored('Files Loaded.', 'green'))

from src import search
search.load_index()
print(colored('Index Loaded.', 'green'))

from flask import Flask, request, render_template
app = Flask(__name__)

def retrieve(query):
	"""
	Main function for communications
	between web and back-end
	"""
	#Place holder loren ipsum
	# title = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc maximus.'
	# authors = 'Lorem ipsum, dolor sit, amet consectetur.'
	# abstract = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam non consectetur augue. Mauris mollis vitae tortor quis cursus. Vivamus imperdiet quis mauris ut posuere. Integer sit amet blandit erat, in congue dui. Etiam nec sagittis lorem. Vivamus in turpis faucibus, aliquet purus id, consectetur velit. Nulla tristique imperdiet nunc, at auctor enim mattis varius. Vivamus tristique, purus ut convallis aliquam, enim nulla sagittis nisl, eu accumsan risus arcu et velit. Quisque euismod fermentum est vel auctor. Nulla facilisi. Praesent fringilla, est ac porttitor volutpat, mauris tellus facilisis enim, eu aliquet dui urna a diam.'
	results = []
	print(query)
	for id in search.searching(query['freetext']):
		file = id2file[id]
		results.append({'link': 'https://arxiv.org/abs/' + id,
			            'title': file['title'], 
			            'authors': file['authors'], 
			            'abstract': file['abstract']})
	return results
	# return json.dumps(results)

@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        return render_template('results.html', results=retrieve(request.form))
    else:
    	return render_template('base.html')

if __name__ == '__main__':
    app.run()
