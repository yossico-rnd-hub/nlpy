import json
from flask import request, abort
from .action_base import Action
from logger import logger
from nlp import Nlpy
from nlp.wordmap.wordmap import Wordmap
from nlp.json.json_model import Document, Entity, Relation, Span


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
        default_model = 'en'  # default model
        model = request.json['model'] if (
            'model' in request.json) else default_model

        # get the method from request
        method = request.json['method'] if ('method' in request.json) else None

        # load model
        nlp = Nlpy.load(model)

        # get the text
        text = request.json['text']

        # create word map
        try:
            wmap = Wordmap(text, nlp, method=method)
        except Exception as ex:
            logger.exception(ex)
            return json.dumps({"error": ex.args}), 500

        # serialize doc entities to json
        return json.dumps(wmap.words, indent=4, default=lambda x: x.__dict__), 200
