import spacy


class EN_EntityRules(object):
    '''
    match entities based on rules
    e.g: 
    - Hillary killed David.
        spacy: ( Hillary/ORG, killed, David/PERSON )
    - Hillary is the step mother of Chelsea.
        spacy: ( Hillary/ORG, step mother, Chelsea/ORG )
    '''

    name = 'en-ent-rules'

    def __init__(self):
        pass

    def __call__(self, doc, entities):
        # lilo:TODO
        return doc
