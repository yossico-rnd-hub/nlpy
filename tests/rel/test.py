#!env/bin/python

'''
extract relations between entities
'''

import sys
sys.path.append('.')

import argparse

import spacy
from spacy.tokens import Doc

from gold import Gold
from corpus_en import CORPUS_EN
from corpus_es import CORPUS_ES

from ent import EntitiesPipeline
from ent.lang.en import EN_EntityMatcher
from ent.lang.en import EN_EntityRules

from rel import RelationPipeline
from rel.lang.en import EN_SPO_RelationExtractor
from rel.lang.en import EN_IS_A_RelationExtractor
from rel.lang.es import ES_SPO_RelationExtractor

__model = 'en'  # 'en'/'es'


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


def is_spanish(model):
    return model.startswith('es')


def main(model, text, id):
    nlp = spacy.load(model)
    print("Loaded model '%s'" % model)

    # entities pipeline
    ent_pipeline = EntitiesPipeline()
    nlp.add_pipe(ent_pipeline, after='ner')

    # relations pipeline
    rel_pipeline = RelationPipeline()
    nlp.add_pipe(rel_pipeline, last=True)

    if (text):
        CORPUS = [{'text': text, 'relations': []}]
    elif is_spanish(model):
        CORPUS = CORPUS_ES
        # es relations
        rel_pipeline.add_pipe(ES_SPO_RelationExtractor())
    else:
        CORPUS = CORPUS_EN

        # en entities
        ent_pipeline.add_pipe(EN_EntityRules())
        ent_pipeline.add_pipe(EN_EntityMatcher(nlp))

        # en relations
        rel_pipeline.add_pipe(EN_SPO_RelationExtractor())
        rel_pipeline.add_pipe(EN_IS_A_RelationExtractor())

    print("Processing %d texts" % len(CORPUS))
    print()

    show_warning = False
    for sample in CORPUS:

        if (id > 0 and id != sample['id']):
            continue  # skip

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

            if (len(doc.ents) == 0):
                print('No entities!')
            else:
                print('entities:')
                for e in doc.ents:
                    print('  {}/{}'.format(e.text, e.label_))

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
    _argparser = argparse.ArgumentParser(
        description='test nlp-service entity extraction.')
    _argparser.add_argument('-i', '--id', type=int,
                            help='document id to process')
    _argparser.add_argument('-t', '--text', help='text to process')
    _argparser.add_argument('-m', '--model', help='model to use')

    args = _argparser.parse_args()
    text = args.text if args.text else None
    model = args.model if args.model else __model
    id = args.id if args.id else -1

    main(model=model, text=text, id=id)
