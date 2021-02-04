from flask import Flask, request, render_template
app = Flask(__name__)

def retrieve(query):
	"""
	Main function for communications
	between web and back-end
	"""
	#Place holder loren ipsum
	title = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc maximus.'
	authors = 'Lorem ipsum, dolor sit, amet consectetur.'
	abstract = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam non consectetur augue. Mauris mollis vitae tortor quis cursus. Vivamus imperdiet quis mauris ut posuere. Integer sit amet blandit erat, in congue dui. Etiam nec sagittis lorem. Vivamus in turpis faucibus, aliquet purus id, consectetur velit. Nulla tristique imperdiet nunc, at auctor enim mattis varius. Vivamus tristique, purus ut convallis aliquam, enim nulla sagittis nisl, eu accumsan risus arcu et velit. Quisque euismod fermentum est vel auctor. Nulla facilisi. Praesent fringilla, est ac porttitor volutpat, mauris tellus facilisis enim, eu aliquet dui urna a diam.'
	results = []
	for _ in range(30):
		results.append({'title': title, 'authors': authors, 'abstract': abstract})
	return results
	# return json.dumps(results)

@app.route('/', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        return render_template('results.html', results=retrieve(request.form))
    else:
    	return render_template('base.html')
