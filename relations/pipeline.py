#!env/bin/python

'''
extract relations between entities
'''

from __future__ import unicode_literals, print_function

import spacy
from spacy.tokens import Doc


class RelationPipeline(object):
    pipe_ = []

    def __init__(self):
        Doc.set_extension('relations', default=[])

    def __call__(self, doc):
        modified_doc = doc
        for c in self.pipe_:
            modified_doc = c(doc)
        return modified_doc

    def add_pipe(self, component):
        self.pipe_.append(component)
