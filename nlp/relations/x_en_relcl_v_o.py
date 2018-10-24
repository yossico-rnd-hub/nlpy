import spacy
from .util import is_xsubj, filter_subj, filter_obj, _extend_lefts, _right_conj, create_relation


class EN_RELCL_V_O_RelationExtractor(object):
    '''
    extract RELCL_V_O relations\n
    e.g: '<Bill/relcl> and Hillary Clinton, parents of Chelsea <married/verb> on October 11, 1975.'
    '''

    name = 'en-relcl-v-o'

    def __init__(self):
        pass

    def __call__(self, doc, relations):
        ''' extracts (relcl, verb, object, when, self.name) '''
        for t in self.relcl_verb_object(doc):
            relations.append(create_relation(*t))
        return doc

    def relcl_verb_object(self, doc):
        ''' extract (subj, verb/dep_ == relcl, object) triples '''
        for verb in filter(lambda t: t.pos_ == 'VERB', doc):
            if (verb.dep_ != 'relcl'):
                continue

            subj = verb.head
            if (not filter_subj(subj)):
                continue  # skip none-entity

            verb = doc[verb.i:verb.i+1]

            for obj in self._extract_objects(verb):
                yield (subj, verb, obj)

            # subj.conj
            for conj in _right_conj(subj):
                for obj in self._extract_objects(verb):
                    yield (conj, verb, obj)

    # lilo:TODO - change (copied from en-svo)
    def _extract_objects(self, verb):
        ''' return objects in (s,v,o) related to given VERB '''

        # rule 1: verb -> dobj
        # (e.g: <PERSON/nsubj> <killed/verb> <PERSON/dobj>)
        for dobj in filter(lambda w: w.dep_ in ('dobj', 'obj'), verb.rights):
            if (not filter_subj(dobj)):
                continue  # skip none-entity
            return [dobj] + _right_conj(dobj)

        # rule 2: verb-span (including: prep/dative/agent) -> pobj
        # (e.g: <PERSON/nsubj> <killed by/verb-span> <PERSON/pobj>)
        for pobj in filter(lambda w: w.dep_ == 'pobj', verb.rights):
            if (not filter_subj(pobj)):
                continue  # skip none-entity
            return [pobj] + _right_conj(pobj)

        # rule 3: verb -> prep/dative/agent -> pobj
        # (e.g: <PERSON/nsubj> <met/verb> <with/prep> <PERSON/pobj>)
        for prep in filter(lambda w: w.dep_ in ('prep', 'dative', 'agent'), verb.rights):
            for pobj in filter(lambda w: w.dep_ in ('pobj'), prep.children):
                if (not filter_obj(pobj)):
                    continue  # skip none-entity
                return [pobj] + _right_conj(pobj)

        obj = next(filter(lambda w: w.dep_ in ('nmod'), verb.rights), None)
        if (obj and filter_obj(obj)):  # skip none-entity
            return [obj] + _right_conj(obj)
        return []  # None
