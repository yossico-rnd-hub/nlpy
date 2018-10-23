import logging
import spacy
from .util import is_xsubj, filter_subj, filter_obj, _extend_lefts, _right_conj, create_relation


class ES_SVO_RelationExtractor(object):
    '''
    extract SPO relations between entities
    '''

    name = 'es-svo'

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
            if (not filter_subj(subj)):
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
                if (not filter_subj(conj)):
                    continue  # skip none-entity
                for obj in self._extract_objects(verb):
                    yield (conj, verb, obj)

    def _extract_verb(self, subj):
        ''' extract the VERB related to the given subject '''
        verb = subj.head
        if (verb.pos_ != 'VERB'):
            return None
        return verb.doc[verb.i:verb.i+1]

    def _extract_objects(self, verb):
        ''' return objects in (s,v,o) related to given VERB '''

        # rule 1: verb -> obl (oblique nominal)
        # (e.g: <PERSON/nsubj> <casaron (married)/verb> <DATE-TIME/obl>)
        obj = next(filter(lambda w: w.dep_ in (
            'obj', 'obl'), verb.rights), None)
        if obj:
            if (not filter_obj(obj)):
                # rule 2: verb -> obj -> <real-obj>/appos
                # e.g: '<reunió/verb> con el -> <congresista/obj> -> <Mike Pence/appos>'
                appos = next(filter(lambda w: w.dep_ ==
                                    'appos', obj.rights), None)
                if (appos and filter_obj(appos)):  # skip none-entity
                    obj = appos
            return [obj] + _right_conj(obj)

        return []  # None
