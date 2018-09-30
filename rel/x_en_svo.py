import logging
import spacy
from rel.util import is_xsubj, _extend_compound, _extend_lefts, _right_conj, create_relation


class EN_SVO_RelationExtractor(object):
    '''
    extract SPO relations between entities
    '''

    name = 'en-svo'

    def __init__(self):
        pass

    def __call__(self, doc, relations):
        ''' extracts (subject, pred, object, when, self.name) '''
        for t in self.subject_verb_object(doc):
            relations.append(create_relation(*t))
        return doc

    def subject_verb_object(self, doc):
        ''' extract (subject, verb, object) triples '''
        for subj in filter(lambda t: is_xsubj(t), doc):
            if (0 == subj.ent_type):
                continue  # skip none-entity
            logging.debug('(x:{}) subj: {}'.format(self.name, subj))

            verb = self._extract_verb(subj)
            if (None == verb):
                continue
            logging.debug('(x:{}) verb: {}'.format(self.name, verb))

            for obj in self._extract_objects(verb):
                logging.debug('(x:{}) obj: {}'.format(self.name, obj))
                yield (subj, verb, obj)

            # subj.conj
            for conj in _right_conj(subj):
                if (0 == conj.ent_type):
                    continue  # skip none-entity
                for obj in self._extract_objects(verb):
                    yield (conj, verb, obj)

    def _extract_verb(self, s):
        ''' try to extract the VERB related to the given subject '''
        verb = s.head

        if (verb.pos_ != 'VERB'):
            return None

        # verb expansion rules

        # rule 1: '... <started/advcl> <-> <working/xcomp> at Google...'
        if (verb.dep_ == 'advcl'):
            right_verb = next(
                filter(lambda w: w.pos_ == 'VERB' and w.dep_ == 'xcomp', verb.rights), None)
            if (None != right_verb):
                return verb.doc[verb.i: right_verb.i+1]

        # rule 2: <PERSON/nsubj> <killed/VERB> <by/agent> <PERSON/pobj>
        for w in verb.rights:
            if (w.dep_ in ('agent')):
                return verb.doc[verb.i:w.i + 1]

        # rule 3: <PERSON/nsubj> <is/VERB> the <president/attr> of
        for w in verb.rights:
            if (w.dep_ in ('attr')):
                return _extend_lefts(w)

        # rule 4: merge verb with dobj if none entity
        dobj = next(filter(lambda w: w.dep_ in (
            'dobj', 'obj'), verb.rights), None)
        if (None != dobj):
            # 4.1 - dative: '<PERSON/nsubj> <gave/VERB> <testimony/dobj> <to/dative> ...'
            for w in verb.rights:
                if (w.dep_ in ('dative')):
                    return verb.doc[verb.i:dobj.i + 1]
            # 4.2 - prep: '<PERSON/nsubj> <had/VERB> a <debate/dobj> <with/prep> <PERSON/pobj>...'
            for w in dobj.rights:
                if (w.dep_ in ('prep', 'nmod')):
                    return verb.doc[dobj.i:dobj.i+1]

        return verb.doc[verb.i:verb.i+1]

    def _extract_objects(self, verb):
        ''' return objects in (s,v,o) related to given VERB '''

        # rule 1: verb -> dobj
        # (e.g: <PERSON/nsubj> <killed/verb> <PERSON/dobj>)
        dobj = next(filter(lambda w: w.dep_ in (
            'dobj', 'obj'), verb.rights), None)
        if (None != dobj and 0 != dobj.ent_type):  # skip none-entity
            return [dobj] + _right_conj(dobj)

        # rule 2: verb-span (including: prep/dative/agent) -> pobj
        # (e.g: <PERSON/nsubj> <killed by/verb-span> <PERSON/pobj>)
        pobj = next(filter(lambda w: w.dep_ == 'pobj', verb.rights), None)
        if (None != pobj and 0 != pobj.ent_type):  # skip none-entity
            return [pobj] + _right_conj(pobj)

        # rule 3: verb -> prep/dative/agent -> pobj
        # (e.g: <PERSON/nsubj> <met/verb> <with/prep> <PERSON/pobj>)
        for prep in filter(lambda w: w.dep_ in ('prep', 'dative', 'agent'), verb.rights):
            pobj = next(filter(lambda w: w.dep_ ==
                               'pobj', prep.children), None)
            if (None != pobj and 0 != pobj.ent_type):  # skip none-entity
                return [pobj] + _right_conj(pobj)

        obj = next(filter(lambda w: w.dep_ in ('nmod'), verb.rights), None)
        if (None != obj and 0 != obj.ent_type):  # skip none-entity
            return [obj] + _right_conj(obj)
        return []  # None
