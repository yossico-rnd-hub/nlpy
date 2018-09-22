#!env/bin/python

'''
extract SPO relations between entities
'''

from __future__ import unicode_literals, print_function

import spacy
from spacy.tokens import Doc
from rel.parse_util import root, is_root, is_xsubj


class ES_SPO_RelationExtractor(object):
    name = 'es_rel_spo'

    def __init__(self):
        pass

    def __call__(self, doc, relations):
        # try to extract relations from all entity types available in the document
        subj_e_types = list(set(e.label_ for e in doc.ents))

        for e in filter(lambda w: w.ent_type_ in subj_e_types, doc):
            if (is_xsubj(e)):
                pred = e.head
                obj = next(filter(
                    lambda w: w != e and w.pos_ in ('NOUN', 'PROPN'), pred.children), None)
                if (None != obj):
                    relations.append((e, pred, obj, None))  # matched
            elif (is_root(e)):
                pred = next(filter(
                    lambda w: w != e and w.pos_ in ('VERB', 'NOUN', 'PROPN'), e.children), None)
                if (None != pred):
                    obj = next(filter(
                        lambda w: w != e and w.pos_ in ('NOUN', 'PROPN'), pred.children), None)
                    if (None != obj):
                        relations.append((e, pred, obj, None))  # matched
        return doc
