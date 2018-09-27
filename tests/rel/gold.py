#!env/bin/python

'''
relation gold grader
add one or more docs
get scoring for a single doc or scoring of all docs
'''

from tests.scoring import Scoring


class Gold(object):
    def __init__(self):
        self._dict = {}

    def add(self, doc, id, gold_relations):
        if (id in self._dict):
            return None

        scoring = Scoring()
        self._dict[id] = (doc, scoring)

        doc_relations = list(
            map(lambda r: self._relation_to_string_tuple(r), doc._.relations))

        if (len(doc_relations) == 0 and len(gold_relations) == 0):
            return scoring  # empty match

        for r in doc_relations:
            if (r in gold_relations):
                scoring.true_positives += 1
            else:
                scoring.false_positives += 1

        for r in gold_relations:
            if (r not in doc_relations):
                scoring.false_negatives += 1

        return scoring

    def doc_scoring(self, id):
        '''get scoring for doc by id'''
        if (not id in self._dict):
            return None
        _, scoring = self._dict[id]
        return scoring

    def scoring(self):
        '''get overall scoring for all docs'''
        scoring = Scoring()  # overall scoring
        for id in self._dict:
            _, s = self._dict[id]
            scoring.true_positives += s.true_positives
            scoring.false_positives += s.false_positives
            scoring.false_negatives += s.false_negatives
        return scoring

    def _relation_to_string_tuple(self, r):
        s, p, o, w = r
        return (s.text, p.text, o.text, w.text if w else None)
