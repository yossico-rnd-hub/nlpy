#!nlp/bin/python
from flask import Flask, request, jsonify, abort
from datetime import datetime
from nlp import Nlp, Document
import json

app = Flask(__name__)

nlp = Nlp('en')

@app.route('/')
def home():
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    return "nlp-service ready.<br>" + formatted_now

@app.route('/api/v1.0/docs', methods=['POST'])
def process_doc():
    # text is a required field
    if not request.json or not 'text' in request.json:
        abort(400) # bad request

    # doc = request.json

    #lilo: test
    doc = Document()
    doc.text = (u"When Sebastian Thrun started working on self-driving cars at "
            u"Google in 2007, few people outside of the company took him "
            u"seriously. “I can tell you very senior CEOs of major American "
            u"car companies would shake my hand and turn away because I wasn’t "
            u"worth talking to,” said Thrun, now the co-founder and CEO of "
            u"online higher education startup Udacity, in an interview with "
            u"Recode earlier this week.")
    
    res = nlp.process(doc)
    return json.dumps(res.entities, indent=4, default=lambda x: x.__dict__), 200

if __name__ == '__main__':
    app.run(debug=True)
