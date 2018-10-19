#!env/bin/python

'''
relation gold grader
add one or more docs
get scoring for a single doc or scoring of all docs
'''

import spacy
from spacy.lang.en import English
from tests.scoring import Scoring
from nlp.relations.relation import Relation, Relations


class Gold(object):
    def __init__(self, nlp):
        self.nlp = nlp
        self._dict = {}

    def add(self, doc, id, gold_relation_tuples):
        if (id in self._dict):
            return None

        scoring = Scoring()
        self._dict[id] = (doc, scoring)

        gold_relations = self.tuples_to_relations(gold_relation_tuples)

        doc_relations = doc._.relations

        if (len(doc_relations) == 0 and len(gold_relations) == 0):
            return scoring  # empty match

        for r in doc_relations:
            if (gold_relations.contains(r)):
                scoring.true_positives += 1
            else:
                scoring.false_positives += 1

        for r in gold_relations:
            if (not doc_relations.contains(r)):
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

    def tuples_to_relations(self, gold_relation_tuples):
        relations = Relations(self.nlp)
        for t in gold_relation_tuples:
            relations.append(Relation(*t))
        return relations
