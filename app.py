from flask import Flask, request, render_template
app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

@app.route('/', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        print(query)
        return render_template('base.html')
    else:
    	return render_template('base.html')
