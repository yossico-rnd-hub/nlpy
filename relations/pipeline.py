#!env/bin/python

'''
extract relations between entities
'''

import spacy
from spacy.tokens import Doc
from .parse_util import root


class RelationPipeline(object):
    name = 'relations'
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

        doc._.relations = list(filter(lambda r: not self.is_neg(r), relations))

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
