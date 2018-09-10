import spacy

import jsonpickle
import jsonpickle.tags as tags
import jsonpickle.unpickler as unpickler
import jsonpickle.util as util

import re

# NER tags pure whitespace as entities #1717
# https://github.com/explosion/spaCy/issues/1717
def remove_whitespace_entities(doc):
    doc.ents = [e for e in doc.ents if not e.text.isspace()]
    return doc

#lilo
do_pre_process_text = False
def pre_process_text(text):
    if (False == do_pre_process_text):
        return text
        
    # (keep paragraph separator) replace 2 or more newlines with tmp '\r\r'
    text = re.sub(r'\n\n+', '\r\r', text)
    # replace newlines with spaces
    text = re.sub(r'\n', ' ', text)
    # restore paragraph separator ('\r\r' -> '\n\n')
    text = re.sub(r'\r\r', '\n\n', text)
    return text

class Document(object):
    """Document class"""
    def __init__(self, text = ''):
        self.text = text
        self.entities = []

    def from_json_file(self, file):
        '''load from json file'''
        with open(file, 'r') as f:
            doc_json = f.read()
            self.from_json(doc_json)
    
    def from_json(self, json):
        '''load from json string'''
        doc_dict = jsonpickle.decode(json)
        self.text = doc_dict['text']
        self.entities = []
        for e_dict in doc_dict['entities']:
            e_dict[tags.OBJECT] = util.importable_name(Entity)
            e = unpickler.Unpickler().restore(e_dict, classes=[Entity])
            self.entities.append(e)

    def entities_from_json(self, json):
        '''
        read from entities json
        returns entities list
        '''
        entities_dict = jsonpickle.decode(json)
        entities = []
        for e_dict in entities_dict:
            e_dict[tags.OBJECT] = util.importable_name(Entity)
            e = unpickler.Unpickler().restore(e_dict, classes=[Entity])
            entities.append(e)
        return entities

class Entity(object):
    """Entity class"""
    def __init__(self, text = '', start_char = -1, end_char = -1, label = ''):
        self.text = text
        self.label = label
        self.start_char = start_char
        self.end_char = end_char

class Nlp(object):
    """Nlp class"""
    def __init__(self, language = 'en_core_web_lg'):
        # Load English tokenizer, tagger, parser, NER and word vectors
        self.nlp = spacy.load(language)
        self.nlp.add_pipe(remove_whitespace_entities, after='ner')

    def process(self, doc):
        # Process whole documents
        doc.text = pre_process_text(doc.text)
        spacy_doc = self.nlp(doc.text)

        for ent in spacy_doc.ents:
            e = Entity(ent.text, ent.start_char, ent.end_char, ent.label_)
            doc.entities.append(e)
        return doc
