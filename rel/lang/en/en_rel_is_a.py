'''
extract IS_A/is_not relations between entities
'''


import spacy
from spacy.tokens import Doc
from rel.parse_util import root, is_xsubj


class EN_IS_A_RelationExtractor(object):
    name = 'en_rel_is_a'

    def __init__(self):
        pass

    def __call__(self, doc, relations):
        # try to extract relations from all entity types available in the document
        if (len(doc.ents) == 0):
            return doc
        subj_e_types = list(set(e.label_ for e in doc.ents))

        for e in filter(lambda w: w.ent_type_ in subj_e_types, doc):
            if is_xsubj(e):
                rt = root(e)
                if (rt.lemma_ == 'be' or rt.lemma_ == 'do'):  # is/did
                    pred_span = self.extract_is_a_pred_span(e)
                    if (None != pred_span):
                        for obj in self.extract_is_a_object(e):
                            relations.append((e, pred_span, obj, None))
            return doc

    def extract_is_a_pred_span(self, subj):
        pred = None
        rt = root(subj)
        pred = next(filter(lambda w: w.dep_ == 'attr', rt.rights), None)
        if (None == pred):
            return None
        i = pred.i
        for x in filter(lambda w: w.dep_ in ('compound', 'amod'), pred.lefts):
            i = min(x.i, i)
        pred_span = pred.doc[i:pred.i+1]
        return pred_span

    def extract_is_a_object(self, subj):
        ''' extract (s,p,o) objects '''
        obj_list = []
        rt = root(subj)
        attr = next(filter(lambda w: w.dep_ == 'attr', rt.rights), None)
        if (None != attr):
            prep = next(filter(lambda w: w.dep_ == 'prep', attr.rights), None)
            if (None != prep):
                pobj = next(filter(
                    lambda w: w.dep_ == 'pobj', prep.rights), None)
                while (None != pobj):  # handle multiple objects ?
                    obj_list.append(pobj)
                    pobj = next(filter(
                        lambda w: w.dep_ == 'conj', pobj.rights), None)

        return obj_list
