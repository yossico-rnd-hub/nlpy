#!nlp/bin/python
from flask import Flask, request, jsonify, abort
from datetime import datetime
from nlp import Nlp, Document
import json

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

nlp = Nlp(model = 'en_core_web_sm')
# nlp = Nlp(model = 'es')

@app.route('/')
def home():
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    return "nlp-service ready.<br>" + formatted_now

@app.route('/api/v1.0/docs', methods=['POST'])
def process_doc():
    '''
    Extract entities\n
    Usage: curl -i -H "Content-Type: application/json" -X POST -d '{"text": "foo"}' http://localhost:5000/api/v1.0/docs
    '''
    # text is a required field
    if not request.json or not 'text' in request.json:
        abort(400) # bad request

    # process the document 
    doc = Document()
    doc.text = request.json['text']
    
    res = nlp.process(doc)
    return json.dumps(res.entities, indent=4, default=lambda x: x.__dict__), 200

if __name__ == '__main__':
    app.run(debug=True)
