'''
a pipeline for extracting entity relations.

you can add relations extraction to nlp.pipeline using:
    rel_pipeline = RelationPipeline()
    nlp.add_pipe(rel_pipeline, after='ner')

you can add your relation extrators (one or more) using:
    rel_pipeline.add_pipe(YOUR_RelationExtractor())

'''

import spacy
from spacy.tokens import Doc
from .parse_util import root


class RelationPipeline(object):
    name = 'ws_relations'
    pipe_ = []

    def __init__(self):
        Doc.set_extension('relations', default=[])

    def __call__(self, doc):
        # merge entities into one token
        spans = list(doc.ents)
        for span in spans:
            span.merge()

        relations = []
        for c in self.pipe_:
            doc = c(doc, relations)

        relations = list(filter(lambda r: not self.is_neg(r), relations))
        doc._.relations = relations
        return doc

    def add_pipe(self, component):
        self.pipe_.append(component)

    def is_neg(self, r):
        _, p, _, _ = r
        rt = root(p)
        for w in rt.children:
            if (w.dep_ == 'neg'):
                return True
        return False
