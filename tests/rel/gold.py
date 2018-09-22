#!env/bin/python

'''
gold grader
'''

from __future__ import unicode_literals, print_function

import spacy
from spacy.tokens import Doc


class Gold(object):
    def __init__(self, doc, gold_relations):
        doc_relations = list(
            map(lambda r: self.relation_to_string_tuple(r), doc._.relations))

        if (len(doc_relations) == 0 and len(gold_relations) == 0):
            # empty match
            self.precision = 1.0
            self.recall = 1.0
            self.f1score = 1.0
            return

        true_positives = 0
        false_positives = 0
        false_negatives = 0

        for r in doc_relations:
            if (r in gold_relations):
                true_positives += 1
            else:
                false_positives += 1

        for r in gold_relations:
            if (r not in doc_relations):
                false_negatives += 1

        precision = true_positives / (true_positives + false_positives) \
            if (true_positives + false_positives > 0) else 0.0
        recall = true_positives / (true_positives + false_negatives) \
            if (true_positives + false_negatives > 0) else 0.0
        f1score = 2 * (precision * recall) / (precision + recall) \
            if (precision + recall > 0) else 0.0

        self.precision = precision
        self.recall = recall
        self.f1score = f1score

    def relation_to_string_tuple(self, r):
        s, p, o, w = r
        return (s.text, p.text, o.text, w.text if w else None)
