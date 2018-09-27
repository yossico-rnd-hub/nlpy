import spacy
from spacy.tokens import Doc

from rel.when import extract_when
from rel.util import is_xsubj, _extend_entity_name, _extend_lefts, _right_conj


class SVO_RelationExtractor(object):
    '''
    extract SPO relations between entities
    '''

    name = 'svo'

    def __init__(self):
        pass

    def __call__(self, doc, relations):
        ''' extracts (subject, verb, object, when, self.name) '''
        for t in self.subject_verb_object(doc):
            s, v, o = t
            when = extract_when(v)
            relations.append((s, v, o, when))
        return doc

    def subject_verb_object(self, doc):
        ''' extract (subject, verb, object) triples '''
        for subj in self._extract_subjects(doc):
            verb = self._extract_verb(subj)
            for obj in self._extract_objects(verb):
                yield (subj, verb, obj)

    def _extract_subjects(self, doc):
        for s in filter(lambda t: is_xsubj(t), doc):
            if (0 == s.ent_type):
                continue  # skip none-entity
            subj = _extend_entity_name(s)
            yield subj

    def _extract_verb(self, s):
        ''' try to extract the VERB related to the given subject '''
        verb = s[-1].head

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
        for dobj in filter(lambda w: w.dep_ in ('dobj', 'obj'), verb.rights):
            if (0 == dobj.ent_type):
                continue  # skip none-entity
            return _right_conj(_extend_entity_name(dobj))

        # rule 2: verb-span (including: prep/dative/agent) -> pobj
        # (e.g: <PERSON/nsubj> <killed by/verb-span> <PERSON/pobj>)
        for pobj in filter(lambda w: w.dep_ == 'pobj', verb.rights):
            if (0 == pobj.ent_type):
                continue  # skip none-entity
            return _right_conj(_extend_entity_name(pobj))

        # rule 3: verb -> prep/dative/agent -> pobj
        # (e.g: <PERSON/nsubj> <met/verb> <with/prep> <PERSON/pobj>)
        for prep in filter(lambda w: w.dep_ in ('prep', 'dative', 'agent'), verb.rights):
            for pobj in filter(lambda w: w.dep_ in ('pobj'), prep.children):
                if (0 == pobj.ent_type):
                    continue  # skip none-entity
                return _right_conj(_extend_entity_name(pobj))

        for obj in filter(lambda w: w.dep_ in ('nmod'), verb.rights):
            if (0 == obj.ent_type):
                continue  # skip none-entity
            return _right_conj(_extend_entity_name(obj))
        return []  # None
