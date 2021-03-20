from termcolor import colored

"""
dict_keys(['id', 'submitter', 'authors', 'title', 'comments', 
'journal-ref', 'doi', 'report-no', 'categories', 'license', 
'abstract', 'versions', 'update_date', 'authors_parsed', 'content'])
"""
import boto3
import os

print(colored('Downloading indexes...', 'red'))
session = boto3.session.Session()
client = session.client('s3',
                        region_name='ams3',
                        endpoint_url='https://ams3.digitaloceanspaces.com',
                        aws_access_key_id=os.getenv('SPACES_KEY'),
                        aws_secret_access_key=os.getenv('SPACES_SECRET'))

client.download_file('arxiver-data',
                     'ttds_data.tar',
                     '/workspace/src/ttds_data.tar')

print(colored('Indexes downloaded.', 'green'))

print(colored("Extracting indexes...", "red"))
import subprocess
subprocess.run(["sh", "prep.sh"])
print(colored("Indexes processed.", "green"))

from src import utils
vocab = utils.get_vocabulary()
citations = utils.get_citations()
print(colored("Loaded vocab and citations.", "green"))

import arxiv
# import json
# with open('arxiv_sampled.json', 'r') as f:
#     example = json.loads(f.read())
# id2file = dict()
# for paper in example['papers']:
#     id2file[paper['id']] = paper
# print(colored('Files Loaded.', 'green'))

from src import search
# search.load_index()
# print(colored('Index Loaded.', 'green'))

from flask import Flask, request, render_template
app = Flask(__name__)

import time
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
	ids = search.searching(query['freetext'])[:100]
	start = time.time()
	for i, file in enumerate(arxiv.query(id_list=ids)):
		try:
			suff = "..." if len(file["authors"]) > 5 else ''
			results.append({'link': 'https://arxiv.org/abs/' + ids[i],
				            'title': file['title'], 
				            'authors': ', '.join(file['authors'][:5]) + suff, 
				            'abstract': file['summary']})
		except:
			print(id, ' does not work!')
	end = time.time()
	print('arxiv requests took %.3f seconds for query' % (end-start))
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
