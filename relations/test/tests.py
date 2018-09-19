#!env/bin/python

'''
extract relations between entities
'''

import sys
sys.path.append('.')

import spacy
from spacy.tokens import Doc

from gold import Gold
from corpus_en import CORPUS_EN
from corpus_es import CORPUS_ES

from relations import RelationPipeline
from relations.lang.en import EN_SPO_RelationExtractor
from relations.lang.en import EN_IS_A_RelationExtractor
from relations.lang.es import ES_SPO_RelationExtractor

__model = 'en'  # 'en'/'es'


def is_spanish():
    return __model.startswith('es')


def is_english():
    return __model.startswith('en')


class bcolors:
    DEFAULT = '\033[0m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main(model='en'):
    nlp = spacy.load(model)
    print("Loaded model '%s'" % model)

    # add relations extraction to nlp.pipeline
    rel_pipeline = RelationPipeline()

    if is_spanish():
        CORPUS = CORPUS_ES
        rel_pipeline.add_pipe(ES_SPO_RelationExtractor())
    else:
        CORPUS = CORPUS_EN
        rel_pipeline.add_pipe(EN_IS_A_RelationExtractor())
        rel_pipeline.add_pipe(EN_SPO_RelationExtractor())

    nlp.add_pipe(rel_pipeline, after='ner')

    print("Processing %d texts" % len(CORPUS))
    print()

    show_warning = False
    for sample in CORPUS:

        text = sample['text']
        print(text)
        doc = nlp(text)

        num_found = 0
        for s, p, o, w in doc._.relations:
            num_found += 1
            if (None != w):
                print('( {}/{}, {}, {}/{}, {} )'
                      .format(s.text, s.ent_type_, p.text, o.text, o.ent_type_, w.text))
            else:
                print('( {}/{}, {}, {}/{} )'
                      .format(s.text, s.ent_type_, p.text, o.text, o.ent_type_))

        if (0 == num_found):
            print('No relations!')

        # gold scoring for this document
        gold_relations = sample['relations']
        gold = Gold(doc, gold_relations)

        if (gold.f1score < 1.0):
            show_warning = True
            COLOR = bcolors.WARNING
        else:
            COLOR = bcolors.DEFAULT

        print(COLOR + 'f1score: {} (precision: {}, recall: {})'.format(
            gold.f1score, gold.precision, gold.recall))

        COLOR = bcolors.DEFAULT
        print(COLOR)

    if (len(CORPUS) >= 2):
        if (show_warning):
            print(bcolors.WARNING + "some didn't pass!")
        else:
            print(bcolors.OKGREEN + 'all OK.')


if __name__ == '__main__':
    main(model=__model)
