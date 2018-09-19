#!env/bin/python

'''
extract SPO relations between entities
'''

import spacy
from spacy.tokens import Doc

from relations.parse_util import root, is_xsubj
from .en_rel_util import en_extract_when


class EN_SPO_RelationExtractor(object):
    name = 'en_rel_spo'

    def __init__(self):
        pass

    def __call__(self, doc, relations):
        # try to extract relation subjects from all entity types available in the document
        subj_e_types = list(set(e.label_ for e in doc.ents))

        for e in filter(lambda w: w.ent_type_ in subj_e_types, doc):
            # {PERSON/compound} debate/noun with {PERSON/x}
            if (is_xsubj(e) or (e.dep_ == 'compound')):

                pred = e.head

                if (pred.dep_ == 'advcl'):
                    xcomp = next(filter(
                        lambda w: w.dep_ == 'xcomp', pred.rights), None)
                    if (None != xcomp):
                        pred = xcomp

                self.extract_preposition_relations(e, doc, relations)

                pred_span = self.try_to_extend_pred(pred)

                for obj in self.extract_spo_objects(e, pred):
                    relations.append(
                        (e, pred_span, obj, en_extract_when(pred)))
        return doc

    def try_to_extend_pred(self, pred):
        '''
        try to extend (VERB) predicate if possible\n
        e.g: 'killed by', 'gave testimony', etc. (but not 'killed Bill')
        return pred/perd_span
        '''

        pred_rights = list(pred.rights)
        if (pred.pos_ == 'VERB'):

            if (pred.dep_ == 'xcomp'):
                # '... <started working> at Google...'
                return pred.doc[pred.head.i: pred.i+1]

            for w in pred_rights:
                if (w.ent_type > 0):
                    continue  # do NOT merge entities with pred
                if (w.dep_ in ('agent', 'dobj', 'xcomp')):
                    pred = pred.doc[pred.i: w.i+1]  # merge with pred
        return pred

    # e.g: '... Hillery, mother of Chelsea, ...'
    def extract_preposition_relations(self, e, doc, relations):
        '''
        extract (e1, preposition, e2) relations
        e.g: (... <nsubj>, mother of <pobj>, ...) or (... <nsubj>, employee of <pobj>, ...)
        '''
        pred = next(filter(lambda w: w.dep_ == 'appos', e.children), None)
        if (pred):
            prep = next(filter(lambda w: w.dep_ == 'prep', pred.rights), None)
            if (None != prep):
                pred = doc[pred.i: prep.i + 1]
            objects = [w for w in pred.subtree if w .dep_ in ('pobj', 'conj')]
            for obj in objects:
                r = (e, pred, obj, en_extract_when(pred))
                relations.append(r)

    def extract_spo_objects(self, subj, pred):
        ''' extract (s,p,o) objects '''

        # rule 1: pred -> dobj
        # (e.g: <PERSON/subj> <killed/pred> <PERSON/dobj>)
        obj_list = list(filter(
            lambda w: w.dep_ == 'dobj' and w.ent_type > 0, pred.children))
        if (len(obj_list) > 0):
            return obj_list

        # rule 2: pred -> prep/dative/agent -> pobj
        # (e.g: <PERSON/subj> <met/pred> <with/prep> <PERSON/pobj>)
        obj_list = []
        for prep in filter(lambda w: w.dep_ in ('prep', 'dative', 'agent'), pred.children):
            if (None != prep):
                obj = next(filter(
                    lambda w: w.dep_ == 'pobj' and w.ent_type > 0, prep.children), None)
                while (None != obj):  # handle multiple objects ?
                    if (obj.ent_type_ != 'DATE'):  # skip date as we add it as when
                        obj_list.append(obj)
                    obj = next(filter(lambda w: w.dep_ ==
                                      'conj', obj.rights), None)

        return obj_list
