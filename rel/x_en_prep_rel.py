import logging
import spacy
from rel.util import is_xsubj, _extend_compound, _right_conj, create_relation, root


class EN_PREP_RelationExtractor(object):
    '''
    extract preposition relations: (<ENTITY>, <NOUN> prep, <ENTITY>) \n
     e.g: '<Hillary/subj> is the <mother/pred> <of/prep> <Chelsea/obj>'
    '''

    name = 'prep-rel'

    def __init__(self):
        pass

    def __call__(self,
                 doc,
                 relations,
                 exclude_negation=True,
                 entities_only=True):
        ''' 
        extracts (subject, pred, object, when, self.name) \n
        e.g: '<Hillary/subj> is the <mother/pred> <of/prep> <Chelsea/obj>' \n
        e.g: '<Mark Zukerberg/subj> is the <co-founder/pred> and <CEO/pred> <of/prep> <Facebook/obj>'
        '''
        for t in self.extract_preposition_relations(doc):
            relations.append(create_relation(*t))
        return doc

    def extract_preposition_relations(self, doc):
        ''' extract (subject, pred, object) triples '''
        # start extraction from prep
        for prep in filter(lambda t: t.dep_ == 'prep', doc):

            # pred: <NOUN/pred> <-- <of/prep>
            pred = prep.head
            if (pred.pos_ != 'NOUN'):
                continue  # skip if not NOUN
            logging.debug('(x:{}) pred: {}'.format(self.name, pred))

            # subj (try searching subj in pred.head)
            subj = pred.head
            if (not is_xsubj(subj)):
                # try searching subj in pred.lefts
                subj = next(pred.lefts, None)
                if (None == subj):
                    # try searching subj in pred.root
                    subj = root(pred)
            if (None == subj):
                continue
            if (0 == subj.ent_type):
                continue  # skip none-entity
            logging.debug('(x:{}) subj: {}'.format(self.name, subj))

            # extract objects and relations
            pred_span = doc[pred.i: prep.i+1]

            for obj in self._extract_prep_objects(prep):
                logging.debug('(x:{}) obj: {}'.format(self.name, obj))
                yield (subj, pred_span, obj)

            # subj.conj
            for conj in _right_conj(subj):
                if (0 == conj.ent_type):
                    continue  # skip none-entity
                for obj in self._extract_prep_objects(prep):
                    yield (conj, pred_span, obj)

    def _extract_pred(self, subj_span):
        '''
        extract (subj, preposition, pobj) relations
        e.g: (... <nsubj>, <mother/appos> <of/prep> <pobj>, ...)
        e.g: (... <nsubj>, <employee/appos> <of/prep> <pobj>, ...)
        '''

        pred = next(filter(
            lambda w: w.dep_ == 'appos', subj_span.rights), None)

        if pred:
            prep = next(filter(lambda w: w.dep_ == 'prep', pred.rights), None)
            if prep:
                pred = subj_span.doc[pred.i: prep.i + 1]
                return pred

        return None

    def _extract_prep_objects(self, prep):
        pobj = next(filter(
            lambda w: w.dep_ in ('pobj', 'conj'), prep.rights), None)
        if (None == pobj):
            return []
        return [pobj] + _right_conj(pobj)
