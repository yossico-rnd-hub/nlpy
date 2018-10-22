import json
from flask import request, abort
from .action_base import Action
from logger import logger
from nlp.summarization.jensim_summarizer import Summarization


class SummarizationAction(Action):
    def __init__(self):
        self.name = __class__.__name__
        self.endpoint = '/nlp/summarization'
        self.methods = ['POST']

    def __call__(self, *args):
        # text is a required field
        if not request.json or not 'text' in request.json:
            abort(400)  # bad request

        # get the text
        text = request.json['text']
        word_count = request.json['word_count']

        # create word map
        try:
            s = Summarization()
            res = s.summarize(text, word_count=word_count)
        except Exception as ex:
            logger.exception(ex)
            return json.dumps({"error": ex.args}), 500

        # serialize doc entities to json
        # return json.dumps(res, indent=4, default=lambda x: x.__dict__), 200
        return res, 200
