#!env/bin/python

'''
a pipeline for extracting entities.

you can add entity extraction to nlp.pipeline using:
    ent_pipeline = EntitiesPipeline()
    nlp.add_pipe(ent_pipeline, after='ner')

you can add your relation extrators (one or more) using:
    ent_pipeline.add_pipe(YOUR_EntityExtractor())

'''

import spacy
from spacy.tokens import Span


class EntitiesPipeline(object):
    name = 'ws_entities'
    pipe_ = []

    def __init__(self):
        pass

    def __call__(self, doc):

        entities = []
        for c in self.pipe_:
            doc = c(doc, entities)

        for e in entities:
            start, end, label = e
            span = Span(doc, start, end, label=label)
            doc.ents = list(doc.ents) + [span]

        return doc

    def add_pipe(self, component):
        self.pipe_.append(component)
