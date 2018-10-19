import json
from logger import logger
from nlp import Nlp, Document
from api.action import Action
from flask import request, abort


class Entities(Action):
    '''
    Extract entities\n
    Usage: curl -i -H "Content-Type: application/json" -X POST -d '{"text": "foo", "model": "en"}' http://localhost:5000/api/v0.0.1/nlp/entities
    '''

    def __init__(self):
        self.name = 'entities'
        self.endpoint = '/api/v0.0.1/nlp/entities'
        self.methods = ['POST']
        self.nlp = Nlp()

    def __call__(self, *args):
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
