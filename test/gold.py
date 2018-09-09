from nlp import Document, Entity

class Scoring(object):
    def __init__(self, precision = 0, recall = 0, fscore = 0):
        self.precision = precision
        self.recall = recall
        self.fscore = fscore

class Gold(Document):
    def __init__(self, goldpath):
        self.goldpath = goldpath

    def test_match(self, e):
        '''
        test if and how much the given entity matches a gold antity.\n
        return a real value in [0,1]
        '''
        #lilo: TODO
        return 0.0

    def score(self, doc):
        '''
        produces a scoring (precision, recall & fscore) for the given doc entities.
        '''
        # lilo:TODO
        # calculate per class, then overall
        true_positives = 0
        false_positives = 0
        true_negatives = 0
        false_negatives = 0

        # for (e in doc.entities):
        #     match = test_match(e)

        scoring = Scoring()
        return scoring

