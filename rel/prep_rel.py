import spacy
from spacy.tokens import Doc

from rel.util import is_xsubj, _extend_entity_name, _right_conj, create_relation


class PREP_RelationExtractor(object):
    '''
    extract preposition relations
    '''

    name = 'prep_rel'

    def __init__(self):
        pass

    def __call__(self,
                 doc,
                 relations,
                 exclude_negation=True,
                 entities_only=True):
        ''' 
        extracts (subject, verb, object, when, self.name) \n
        e.g: '<Hillery/subj> is the <mother/pred> <of/prep> <Chelsea/obj>' \n
        e.g: '<Mark Zukerberg/subj> is the <co-founder/pred> and <CEO/pred> <of/prep> <Facebook/obj>'
        '''
        for t in self.extract_preposition_relations(doc):
            relations.append(create_relation(*t))
        return doc

    def extract_preposition_relations(self, doc):
        ''' extract (subject, verb, object) triples '''
        for subj in filter(lambda t: is_xsubj(t), doc):
            if (0 == subj.ent_type):
                continue  # skip none-entity

            pred = self._extract_pred(subj)
            if (None == pred):
                continue

            for obj in self._extract_prep_objects(pred):
                yield (subj, pred, obj)

            # subj.conj
            for conj in _right_conj(subj):
                if (0 == conj.ent_type):
                    continue  # skip none-entity
                for obj in self._extract_prep_objects(pred):
                    yield (conj, pred, obj)

    def _extract_pred(self, subj_span):
        '''
        extract (subj, preposition, pobj) relations
        e.g: (... <nsubj>, <mother/appos> <of/prep> <pobj>, ...)
        e.g: (... <nsubj>, <employee/appos> <of/prep> <pobj>, ...)
        '''

        pred = next(filter(
            lambda w: w.dep_ == 'appos', subj_span.rights), None)

        if (None != pred):
            prep = next(filter(lambda w: w.dep_ == 'prep', pred.rights), None)
            if (None != prep):
                pred = subj_span.doc[pred.i: prep.i + 1]
                return pred

        return None

    def _extract_prep_objects(self, pred_span):
        pobj = next(filter(lambda w: w.dep_ in (
            'pobj', 'conj'), pred_span.rights), None)
        if (None == pobj):
            return None
        return [pobj] + _right_conj(pobj)
