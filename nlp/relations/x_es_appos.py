import logging
import spacy
from .util import is_xsubj, _extend_lefts, _right_conj, create_relation


class ES_APPOS_RelationExtractor(object):
    '''
    extract APPOS relations between entities:\n
    nsubj -> appos <- nmod
    '''

    name = 'es-appos'

    def __init__(self):
        pass

    def __call__(self, doc, relations):
        ''' extracts (subject, pred, object, when, self.name) '''
        for t in self.nsubj_appos_nmod(doc):
            relations.append(create_relation(*t))
        return doc

    def nsubj_appos_nmod(self, doc):
        ''' extract (subject, verb, object) triples '''
        for nsubj in filter(lambda t: is_xsubj(t), doc):
            # nsubj
            if (0 == nsubj.ent_type):
                continue  # skip none-entity

            # pred
            pred = next(filter(lambda w: w.pos_ ==
                               'NOUN' and w.dep_ == 'appos', nsubj.rights), None)
            if (None == pred):
                continue
            pred_span = doc[pred.i:pred.i+1]
            logging.debug('(x:{}) pred: {}'.format(self.name, pred_span))

            # subj.conj
            for subj in [nsubj] + _right_conj(nsubj):
                logging.debug('(x:{}) subj: {}'.format(self.name, subj))

                # obj
                for obj in filter(lambda w: w.dep_ in ('nmod'), pred.rights):
                    logging.debug('(x:{}) obj: {}'.format(self.name, obj))
                    yield (subj, pred_span, obj)
