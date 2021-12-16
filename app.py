from flask import Flask
from flask.templating import render_template
import requests
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
        req = requests.get('https://cat-fact.herokuapp.com/facts')
        data = json.loads(req.content)
        return render_template('index.html', data=data)