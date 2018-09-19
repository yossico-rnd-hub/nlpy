#!env/bin/python

'''
extract IS_A/is_not relations between entities
'''

from __future__ import unicode_literals, print_function


import spacy
from spacy.tokens import Doc
from relations.parse_util import root, is_xsubj
from .en_util import is_or_do_root


class EN_IS_A_RelationExtractor(object):
    name = 'en_rel_is_a'

    def __init__(self):
        pass

    def __call__(self, doc, relations):
        # try to extract relations from all entity types available in the document
        types = list(set(e.label_ for e in doc.ents))
        _subj_e_types = types
        _obj_e_types = types

        for e in filter(lambda w: w.ent_type_ in _subj_e_types, doc):
            if is_xsubj(e):
                if (is_or_do_root(e)):
                    rt = root(e)
                    pred_span = self.en_is_relation_pred_span_from_children(
                        rt.children)
                    for obj in self.en_extract_spo_objects(e, _obj_e_types):
                        relations.append((e, pred_span, obj, None))
            return doc

    def en_is_relation_pred_span_from_children(self, children):
        pred = None
        filtered = filter(lambda w: w.dep_ == 'attr', children)
        list_ = list(filtered)
        if (len(list_) <= 0):
            return None
        pred = list_[-1]  # last one
        i = pred.i
        for x in filter(lambda w: w.dep_ == 'compound', pred.lefts):
            i = min(x.i, i)
        pred_span = pred.doc[i:pred.i+1]
        return pred_span

    # lilo: conj -> multiple objects (also multiple subjects)
    #   '{Donald/compound} {Trump/compound} {debate/ROOT} {with/prep} {Barak/compound} {Obama/pobj} and {Hillary/compound} {Clinton/conj} last Tuesday.'
    def en_extract_spo_objects(self, subj, _obj_e_types):
        ''' extract (s,p,o) objects '''
        obj_list = []
        for e2 in filter(lambda w: w.ent_type_ in _obj_e_types, subj.sent):
            if (e2 == subj):
                continue  # skip subj

            head2 = e2.head
            while (None != head2):
                if (head2 == subj):
                    head2 = head2.head
                    break  # does not match (s,p,o) - missing (,p,) in between

                if (head2 == subj.head):
                    # match
                    obj_list.append(e2)
                    break
                head2 = head2.head

        return obj_list
