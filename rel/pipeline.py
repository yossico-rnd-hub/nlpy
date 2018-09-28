import spacy
from spacy.tokens import Doc
from rel.util import root


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

    def __init__(self):
        Doc.set_extension('relations', default=[])

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
            # filter negative relations
            if self.is_neg(r):
                continue

            # add relation
            filtered.append(r)

        return filtered

    def is_obj_date_time(self, r):
        _, _, o, _ = r
        if (o[0].ent_type_ in ('DATE', 'TIME')):
            return True
        return False

    def is_neg(self, r):
        _, p, _, _ = r
        rt = root(p)
        for w in rt.children:
            if (w.dep_ == 'neg'):
                return True
        return False
