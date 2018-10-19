import logging
import spacy
from relations.util import is_xsubj, _extend_compound, _right_conj, create_relation, root


class ES_NSUBJ_NOUN_NMOD_RelationExtractor(object):
    '''
    extract preposition relations: (<ENTITY/nsubj>, <NOUN>, <ENTITY/nmod>) \n
    e.g: '<Hillary/nsubj> es la <madre/NOUN> del <Chelsea/nmod>'
    '''

    name = 'es-nsubj-noun-nmod'

    def __init__(self):
        pass

    def __call__(self, doc, relations):
        ''' 
        extracts (subject, pred, object, when, self.name) \n
        e.g: '<Bill Clinton/subj> es el <presidente/NOUN> de los <U.S.A/nmod>' \n
        e.g: '<Hillary/nsubj> es la <madre/NOUN> del <Chelsea/nmod>' \n
        e.g: '<Mark Zuckerberg/nsubj> es el <cofundador/NOUN> y <CEO/conj> de <Facebook/nmod>'
        '''
        for t in self.extract_nsubj_noun_nmod_relations(doc):
            relations.append(create_relation(*t))
        return doc

    def extract_nsubj_noun_nmod_relations(self, doc):
        ''' extract (subject, pred, object) triples '''

        # start extraction from nsubj
        for subj in filter(lambda t: is_xsubj(t), doc):
            if (0 == subj.ent_type):
                continue  # skip none-entity
            logging.debug('(x:{}) subj: {}'.format(self.name, subj))

            # pred: <NOUN>
            pred = subj.head
            if (pred.pos_ != 'NOUN'):
                continue  # skip if not NOUN

            # amod: 'el primer presidente'
            start = end = pred.i
            amod = next(filter(lambda w: w.dep_ ==
                               'amod', pred.children), None)
            if amod:
                start = min(pred.i, amod.i)
                end = max(pred.i, amod.i)
            pred_span = doc[start: end+1]
            logging.debug('(x:{}) pred: {}'.format(self.name, pred_span))
            print(list(pred.children))

            # extract objects (nmod) and relations
            for obj in filter(lambda w: w.dep_ == 'nmod', pred.children):
                if (0 == obj.ent_type):
                    continue  # skip none-entity
                logging.debug('(x:{}) obj: {}'.format(self.name, obj))
                yield (subj, pred_span, obj)

            # subj.conj
            for conj in _right_conj(subj):
                if (0 == conj.ent_type):
                    continue  # skip none-entity
                for obj in filter(lambda w: w.dep_ == 'nmod', pred.children):
                    yield (conj, pred_span, obj)
