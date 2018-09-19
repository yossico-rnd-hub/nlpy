#!env/bin/python

'''
extract SPO relations between entities
'''

from __future__ import unicode_literals, print_function

import spacy
from spacy.tokens import Doc


class EN_SPO_RelationExtractor(object):
    name = 'en_rel_spo'

    def __init__(self):
        pass

    def __call__(self, doc):
        return doc
