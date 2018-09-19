#!env/bin/python

'''
extract IS_A relations between entities
'''

from __future__ import unicode_literals, print_function

import spacy
from spacy.tokens import Doc


class EN_IS_A_RelationExtractor(object):
    name = 'en_rel_is_a'

    def __init__(self):
        pass

    def __call__(self, doc):
        return doc
