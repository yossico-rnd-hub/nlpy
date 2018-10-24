import logging
import spacy
from .util import is_xsubj, filter_subj, filter_obj, _extend_lefts, _right_conj, create_relation


class EN_REL_PERSON_ORG(object):
    '''
    extract general relations between PERSON and ORG
    '''

    name = 'en-person-org'

    def __init__(self):
        pass

    def __call__(self, doc, relations):
        for person in filter(lambda e: e.label_ in ('PERSON'), doc.ents):
            for t in self.person_verb_org(doc, person):
                relations.append(create_relation(*t))
            for t in self.person_right_org(doc, person):
                relations.append(create_relation(*t))
        return doc

    def person_verb_org(self, doc, person):
        # TODO
        # if (person[0].head != person[0]):
        #     head_verb = person[0].head
        #     while True:
        #         if (head_verb.pos_ == 'VERB'):
        #             break
        #         head_verb = head_verb.head
        return []

    def person_right_org(self, doc, person):
        # TODO
        pred = doc[person.root.i:person.root.i+1]
        for org in filter(lambda w: w.ent_type_ == 'ORG', person.root.rights):
            yield (person, pred, org)
