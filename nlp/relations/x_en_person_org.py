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
        for person in filter(lambda e: e.label_ == 'PERSON', doc.ents):
            for t in self.person_prep_org(doc, person):
                relations.append(create_relation(*t))
            for t in self.person_lefts_org(doc, person):
                relations.append(create_relation(*t))
            # TODO
            for t in self.person_rights_org(doc, person):
                relations.append(create_relation(*t))
            # TODO
            for t in self.person_verb_org(doc, person):
                relations.append(create_relation(*t))
        return doc

    def person_prep_org(self, doc, person):
        # e.g: '... authored by Peter W. Battaglia of Google's DeepMind'
        prep = next(filter(lambda w: w.dep_ == 'prep', person.rights), None)
        if prep:
            org_iob = []
            for org in filter(lambda w: w.ent_type_ == 'ORG', prep.subtree):
                if (org.ent_iob > 0):
                    org_iob.append(org)
                    if (doc[org.i+1].ent_iob > 0):
                        continue
                    org = doc[org_iob[0].i:org_iob[-1].i + 1]
                yield (person, None, org)

    def person_lefts_org(self, doc, person):
        # e.g: 'NYU professor Gary Marcus'
        pred = next(filter(lambda w: w.pos_ in (
            'NOUN', 'VERB'), person.lefts), None)
        if pred:
            pred = doc[pred.i:pred.i+1]
            for org in filter(lambda w: w.ent_type_ == 'ORG', pred.lefts):
                yield (person, pred, org)

    def person_rights_org(self, doc, person):
        # TODO
        # pred = next(filter(lambda w: w.pos_ in (
        #     'NOUN', 'VERB'), person.rights), None)
        # if pred:
        #     pred = doc[pred.i:pred.i+1]
        #     for org in filter(lambda w: w.ent_type_ == 'ORG', pred.rights):
        #         yield (person, pred, org)

    def person_verb_org(self, doc, person):
        # TODO
        # if (person[0].head != person[0]):
        #     head_verb = person[0].head
        #     while True:
        #         if (head_verb.pos_ == 'VERB'):
        #             break
        #         head_verb = head_verb.head
        return []
