import spacy
import re
from logger import logger

from .entities import EntitiesPipeline
from .relations import RelationPipeline


def remove_whitespace_entities(doc):
    '''
    NER tags pure whitespace as entities \n
    https://github.com/explosion/spaCy/issues/1717
    '''
    doc.ents = [e for e in doc.ents if not e.text.isspace()]
    return doc


class Nlpy(object):
    '''
    model cache with nlpy pipelines for entities/relations
    '''
    models = {}

    @staticmethod
    def load(model):
        '''
        load model using model cache.\n
        add nlpy pipelines for entities/relations
        '''
        if (not model in Nlpy.models):
            try:
                # load model
                nlp = spacy.load(model)
                logger.info("Loaded model '%s'" % model)

                # add nlpy entities pipeline
                nlp.add_pipe(EntitiesPipeline(nlp), after='ner')
                nlp.add_pipe(remove_whitespace_entities, after='nlpy_entities')

                # add nlpy relations pipeline
                nlp.add_pipe(RelationPipeline(nlp), last=True)

                # cache model
                Nlpy.models[model] = nlp
                return nlp
            except Exception as ex:
                error = "Failed to load model: '{}'".format(model)
                logger.error(error)
                logger.exception(ex)
                raise Exception(error)
        else:
            nlp = Nlpy.models[model]
            return nlp

    # lilo: why do we need this?
    @staticmethod
    def pre_process_text(text):
        # (keep paragraph separator) replace 2 or more newlines with tmp '\r\r'
        text = re.sub(r'\n\n+', '\r\r', text)
        # replace newlines with spaces
        text = re.sub(r'\n', ' ', text)
        # restore paragraph separator ('\r\r' -> '\n\n')
        text = re.sub(r'\r\r', '\n\n', text)
        return text
