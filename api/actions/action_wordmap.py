import json
from flask import request, abort
from .action_base import Action
from logger import logger
from nlp import Nlpy
from nlp.json.json_model import Document, Entity, Relation, Span


class Wordmap(object):
    def __init__(self, text, nlp):
        self.create_wordmap(text, nlp)

    def create_wordmap(self, text, nlp):
        self.words = []
        with nlp.disable_pipes('nlpy_relations'):
            doc = nlp(text)
            print(doc.ents)


class WordmapAction(Action):
    def __init__(self):
        self.name = __class__.__name__
        self.endpoint = '/nlp/wordmap'
        self.methods = ['POST']

    def __call__(self, *args):
        # text is a required field
        if not request.json or not 'text' in request.json:
            abort(400)  # bad request

        # get model from request
        default_model = 'en_core_web_sm'  # default model
        model = request.json['model'] if (
            'model' in request.json) else default_model

        # load model
        nlp = Nlpy.load(model)

        # get the text
        text = request.json['text']

        # create word map
        try:
            wmap = Wordmap(text, nlp)
        except Exception as ex:
            logger.exception(ex)
            return json.dumps({"error": ex.args}), 500

        # serialize doc entities to json
        return json.dumps(wmap, indent=4, default=lambda x: x.__dict__), 200
