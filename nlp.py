import spacy

class Document(object):
    """Document class"""
    def __init__(self, text = ''):
        self.text = text
        self.entities = []

class Entity(object):
    """Entity class"""
    def __init__(self, text = '', start_char = -1, end_char = -1, label = ''):
        self.text = text
        self.label = label
        self.start_char = start_char
        self.end_char = end_char

# ent.text, ent.start_char, ent.end_char, ent.label_

class Nlp(object):
    """Nlp class"""
    def __init__(self, language = 'en_core_web_sm'):
        # Load English tokenizer, tagger, parser, NER and word vectors
        self.nlp = spacy.load(language)
        # self.nlp = spacy.load('es')

    def process(self, doc):
        # Process whole documents
        spacy_doc = self.nlp(doc.text)

        for ent in spacy_doc.ents:
            e = Entity(ent.text, ent.start_char, ent.end_char, ent.label_)
            doc.entities.append(e)
        return doc
