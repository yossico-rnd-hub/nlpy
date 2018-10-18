from flask import Flask, request, jsonify, abort
from datetime import datetime
from nlp import Nlp, Document
import json

import logging
logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class EndpointAction(object):
    def __init__(self, action):
        self.action = action

    def __call__(self, *args):
        return self.action()


class NlpyServer(object):
    """Nlpy REST server"""

    def __init__(self):
        self.app = Flask(__name__)
        self.nlp = Nlp()
        self.add_endpoint(endpoint='/', endpoint_name='home',
                          handler=self.home)
        self.add_endpoint(endpoint='/api/v0.0.1/docs', endpoint_name='process_doc',
                          handler=self.process_doc, methods=['POST'])

    def run(self):
        self.app.run(debug=True)

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET']):
        self.app.add_url_rule(endpoint, endpoint_name,
                              EndpointAction(handler), methods=methods)

    def home(self):
        now = datetime.now()
        formatted_now = now.strftime("%A, %d %B, %Y at %X")
        return "nlpy service ready.<br>" + formatted_now

    def process_doc(self):
        '''
        Extract entities\n
        Usage: curl -i -H "Content-Type: application/json" -X POST -d '{"text": "foo", "model": "en"}' http://localhost:5000/api/v0.0.1/docs
        '''
        # text is a required field
        if not request.json or not 'text' in request.json:
            abort(400)  # bad request

        # process the document
        doc = Document()
        doc.text = request.json['text']

        default_model = 'en_core_web_sm'  # default model
        model = request.json['model'] if (
            'model' in request.json) else default_model

        try:
            res = self.nlp.process(doc, model)
        except Exception as ex:
            logger.exception(ex)
            return json.dumps({"error": ex.args}), 500

        return json.dumps(res.entities, indent=4, default=lambda x: x.__dict__), 200
