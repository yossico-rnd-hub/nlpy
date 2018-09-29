import spacy
from spacy.tokens import Doc
from rel.util import root
from rel.relation import Relation, Relations
from rel.x_en_svo import EN_SVO_RelationExtractor
from rel.x_en_prep_rel import EN_PREP_RelationExtractor
from rel.x_en_relcl_v_o import EN_RELCL_V_O_RelationExtractor

from rel.x_es_svo import ES_SVO_RelationExtractor
from rel.x_es_nsubj_noun_nmod import ES_NSUBJ_NOUN_NMOD_RelationExtractor

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

        if (nlp.lang == 'en'):
            self.add_pipe(EN_SVO_RelationExtractor())
            self.add_pipe(EN_PREP_RelationExtractor())
            self.add_pipe(EN_RELCL_V_O_RelationExtractor())
        elif (nlp.lang == 'es'):
            self.add_pipe(ES_SVO_RelationExtractor())
            self.add_pipe(ES_NSUBJ_NOUN_NMOD_RelationExtractor())
        else:
            raise TypeError('language not supported!')

    def __call__(self, doc):
        all_relations = Relations()
        for c in self.pipe_:
            c_relations = Relations()
            doc = c(doc, c_relations)
            for r in c_relations:  # update originating extractor
                r.x = c.name
            all_relations += c_relations
        doc._.relations = self.filter_relations(all_relations)
        return doc

    def add_pipe(self, component):
        self.pipe_.append(component)

    def filter_relations(self, relations):
        filtered = Relations()
        for r in relations:
            # filter out negative relations
            if self.is_neg(r):
                continue

            # add relation
            filtered.append(r)

        return filtered

    def is_neg(self, r):
        rt = root(r.p)
        for w in rt.children:
            if (w.dep_ == 'neg'):
                return True
        return False
