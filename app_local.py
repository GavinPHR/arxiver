from termcolor import colored

"""
dict_keys(['id', 'submitter', 'authors', 'title', 'comments', 
'journal-ref', 'doi', 'report-no', 'categories', 'license', 
'abstract', 'versions', 'update_date', 'authors_parsed', 'content'])
"""

####################################################
# SERVER
####################################################
# import boto3
# import os

# print(colored('Downloading indexes...', 'red'))
# session = boto3.session.Session()
# client = session.client('s3',
#                         region_name='ams3',
#                         endpoint_url='https://ams3.digitaloceanspaces.com',
#                         aws_access_key_id=os.getenv('SPACES_KEY'),
#                         aws_secret_access_key=os.getenv('SPACES_SECRET'))

# client.download_file('arxiver-data',
#                      'ttds_data.tar',
#                      '/workspace/src/ttds_data.tar')

# print(colored('Indexes downloaded.', 'green'))

# print(colored("Extracting indexes...", "red"))
# import subprocess
# subprocess.run(["sh", "prep.sh"])
# print(colored("Indexes processed.", "green"))
####################################################


####################################################
# LOCAL
####################################################
from src import config
config.INDEX_PATH = "ttds_data/indexes"
config.VOCABULARY_PATH = "ttds_data/vocabulary.pbz2"
config.CITATIONS_PATH = "ttds_data/citations.pbz2"
####################################################

print(colored("Loading vocab and citations.", "red"))
from src import utils
vocab = utils.get_vocabulary()
citations = utils.get_citations()
print(colored("Done", "green"))

import arxiv
from src import search

from flask import Flask, request, render_template
app = Flask(__name__)

import time
import calendar
def filter_time(file, from_, to):
	try:
		file_date = time.strptime(file['updated'][:10], '%Y-%m-%d')
		if from_:
			if len(from_) == 4:
				from_ += '-01-01'
			elif len(from_) == 7:
				from_ += '-01'
			from_date = time.strptime(from_, '%Y-%m-%d')
			if file_date < from_date:
				return False
		if to:
			if len(to) == 4:
				to += '-12-31'
			elif len(to) == 7:
				day = calendar.monthrange(int(to[:4]), int(to[-2:]))[1]
				to += '-' + str(day)
			to_date = time.strptime(to, '%Y-%m-%d')
			if file_date > to_date:
				return False
		return True
	except:
		# return False
		return True

def retrieve(query):
	"""
	Main function for communications
	between web and back-end
	"""
	results = []
	ids = search.searching(query['freetext'], 100)
	start = time.time()
	for i, file in enumerate(arxiv.query(id_list=ids)):
		try:
			# print(file)
			if not filter_time(file, query['from'], query['to']):
				continue
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


@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        return render_template('results.html', results=retrieve(request.form))
    else:
    	return render_template('base.html')

if __name__ == '__main__':
    app.run()
