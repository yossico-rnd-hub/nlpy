import spacy
from spacy.tokens import Doc
from rel.util import root
from rel.svo import SVO_RelationExtractor
from rel.prep_rel import PREP_RelationExtractor
from rel.relcl_v_o import RELCL_V_O_RelationExtractor


class RelationPipeline(object):
    '''
    a pipeline for extracting entity relations.

    you can add relations extraction to nlp.pipeline using:
        pipeline = RelationPipeline()
        nlp.add_pipe(pipeline, after='ner')

    you can add your relation extrators (one or more) using:
        pipeline.add_pipe(YOUR_RelationExtractor())

    '''

    name = 'ws_relations'
    pipe_ = []

    def __init__(self, nlp):
        Doc.set_extension('relations', default=[])
        self.add_pipe(SVO_RelationExtractor())
        self.add_pipe(PREP_RelationExtractor())
        self.add_pipe(RELCL_V_O_RelationExtractor())

    def __call__(self, doc):
        relations = []
        for c in self.pipe_:
            doc = c(doc, relations)
        doc._.relations = self.filter_relations(relations)
        return doc

    def add_pipe(self, component):
        self.pipe_.append(component)

    def filter_relations(self, relations):
        filtered = []
        for r in relations:
            # filter out negative relations
            if self.is_neg(r):
                continue

            # add relation
            filtered.append(r)

        return filtered

    def is_neg(self, r):
        _, p, _, _ = r
        rt = root(p)
        for w in rt.children:
            if (w.dep_ == 'neg'):
                return True
        return False
