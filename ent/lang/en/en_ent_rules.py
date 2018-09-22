'''
match entities based on rules
e.g: 
  - Hillery killed David.
    spacy: ( Hillery/ORG, killed, David/PERSON )
  - Hillery is the step mother of Chelsea.
    spacy: ( Hillery/ORG, step mother, Chelsea/ORG )
'''

import spacy
from spacy.tokens import Doc


class EN_EntityRules(object):
    name = 'en_ent_rules'

    def __init__(self):
        pass

    def __call__(self, doc, entities):
        return doc
