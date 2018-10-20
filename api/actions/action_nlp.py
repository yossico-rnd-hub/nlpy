import json
from flask import request, abort
from .action_base import Action
from logger import logger
from nlp import Nlpy
from nlp.json.json_model import Entity


class NLP(Action):
    def __init__(self):
        self.name = __class__.__name__
        self.endpoint = '/nlp'
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

        # process the document
        entities = []
        try:
            doc = nlp(text, model)

            # create result
            for ent in doc.ents:
                e = Entity(ent.text, ent.start_char, ent.end_char, ent.label_)
                entities.append(e)

        except Exception as ex:
            logger.exception(ex)
            return json.dumps({"error": ex.args}), 500

        # serialize doc entities to json
        return json.dumps(entities, indent=4, default=lambda x: x.__dict__), 200
