import spacy
from spacy.tokens import Doc
from .util import root
from .relation import Relation, Relations
from .x_en_svo import EN_SVO_RelationExtractor
from .x_en_prep_rel import EN_PREP_RelationExtractor
from .x_en_relcl_v_o import EN_RELCL_V_O_RelationExtractor
from .x_es_appos import ES_APPOS_RelationExtractor
from .x_en_person_org import EN_REL_PERSON_ORG

from .x_es_svo import ES_SVO_RelationExtractor
from .x_es_nsubj_noun_nmod import ES_NSUBJ_NOUN_NMOD_RelationExtractor


class RelationPipeline(object):
    '''
    a pipeline for extracting entity relations.

    you can add relations extraction to nlp.pipeline using:
        pipeline = RelationPipeline()
        nlp.add_pipe(pipeline, after='ner')

    you can add your relation extrators (one or more) using:
        pipeline.add_pipe(YOUR_RelationExtractor())

    '''

    name = 'nlpy_relations'
    pipe_ = []

    def __init__(self, nlp):
        self.nlp = nlp
        Doc.set_extension('relations', default=[])

        if (nlp.lang == 'en'):
            self.add_pipe(EN_SVO_RelationExtractor())
            self.add_pipe(EN_PREP_RelationExtractor())
            self.add_pipe(EN_RELCL_V_O_RelationExtractor())
            self.add_pipe(EN_REL_PERSON_ORG())
        elif (nlp.lang == 'es'):
            self.add_pipe(ES_SVO_RelationExtractor())
            self.add_pipe(ES_NSUBJ_NOUN_NMOD_RelationExtractor())
            self.add_pipe(ES_APPOS_RelationExtractor())
        else:
            raise TypeError('language not supported!')

    def __call__(self, doc):
        all_relations = Relations(self.nlp)
        for c in self.pipe_:
            c_relations = Relations(self.nlp)
            doc = c(doc, c_relations)
            for r in c_relations:  # update originating extractor
                r.x = c.name
            all_relations += c_relations
        doc._.relations = self.filter_relations(all_relations)
        return doc

    def add_pipe(self, component):
        self.pipe_.append(component)

    def filter_relations(self, relations):
        filtered = Relations(self.nlp)
        for r in relations:
            # filter out negative relations
            if self.is_neg(r):
                continue

            # add relation
            filtered.append(r)

        return filtered

    def is_neg(self, r):
        if (not r.p):
            return False

        rt = root(r.p)
        if (rt.lang_ == 'en'):
            for w in rt.children:
                if (w.dep_ == 'neg'):
                    return True
        elif (rt.lang_ == 'es'):
            for w in r.p[0].children:
                if (w.dep_ == 'advmod' and w.lemma_ == 'no'):
                    return True
        return False
