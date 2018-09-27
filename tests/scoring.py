'''
scoring class to compute precision / recall / f1score
'''


class Scoring(object):
    def __init__(self):
        self.true_positives = 0
        self.false_positives = 0
        self.false_negatives = 0

    def precision(self):
        if (0 == self.false_positives):
            return 1.0

        precision = self.true_positives / (self.true_positives + self.false_positives) \
            if (self.true_positives + self.false_positives > 0) else 0.0
        return precision

    def recall(self):
        if (0 == self.false_negatives):
            return 1.0

        recall = self.true_positives / (self.true_positives + self.false_negatives) \
            if (self.true_positives + self.false_negatives > 0) else 0.0
        return recall

    def f1score(self):
        precision = self.precision()
        recall = self.recall()
        self._f1score = 2 * (precision * recall) / (precision + recall) \
            if (precision + recall > 0) else 0.0
        return self._f1score
