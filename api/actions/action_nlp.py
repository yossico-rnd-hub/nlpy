import json
from flask import request, abort
from .action_base import Action
from logger import logger
from nlp import Nlpy
from nlp.json.json_model import Document, Entity, Relation, Span


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
        default_model = 'en'  # default model
        model = request.json['model'] if (
            'model' in request.json) else default_model

        # load model
        nlp = Nlpy.load(model)

        # get the text
        text = request.json['text']

        process_all = 0 == len(request.args) or 'all' in request.args
        process_entities = process_all or 'entities' in request.args
        process_relations = process_all or 'relations' in request.args

        # process the document
        doc_json = Document()
        doc_json.entities = []
        try:
            doc = nlp(text, model)

            # create result
            if process_entities:
                for ent in doc.ents:
                    e_json = Entity(ent.text, ent.start_char,
                                    ent.end_char, ent.label_)
                    doc_json.entities.append(e_json)

            if process_relations:
                for r in doc._.relations:
                    # lilo:TODO - should we give entities in json_doc an id and use these ids in the relations?
                    # s = Entity(r.s.text, r.s.start_char, r.s.end_char,
                    #            r.s.label_) if r.s else None
                    # p = Span(r.p.text, r.p.start_char, r.p.end_char)
                    # o = Entity(r.o.text, r.o.start_char, r.o.end_char,
                    #            r.o.label_) if r.o else None
                    # w = Entity(r.w.text, r.w.start_char, r.w.end_char,
                    #            r.w.label_) if r.w else None
                    # r_json = Relation(s, p, o, w)
                    doc_json.relations.append(to_tuple(r))

        except Exception as ex:
            logger.exception(ex)
            return json.dumps({"error": ex.args}), 500

        # serialize doc entities to json
        return json.dumps(doc_json, indent=4, default=lambda x: x.__dict__), 200


def to_tuple(r):
    ''' serialize the given relation to a tuple (s,p,o,w) '''
    s = r.s.text if r.s else None
    p = r.p.text if r.p else None
    o = r.o.text if r.o else None
    w = r.w.text if r.w else None
    return (s, p, o, w)
