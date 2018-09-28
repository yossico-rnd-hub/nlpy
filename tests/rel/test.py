#!env/bin/python

'''
test extracting entity relations
'''

import sys
sys.path.append('.')

import argparse

import spacy

from ent import EntitiesPipeline
from rel import RelationPipeline

from tests.rel.gold import Gold
from tests.scoring import Scoring

from corpus_en import CORPUS_EN
from corpus_es import CORPUS_ES

__model = 'en'  # 'en'/'es'


def is_spanish(model):
    return model.startswith('es')


def is_english(model):
    return model.startswith('en')


def ent_types(span):
    if (None == span):
        return None

    res = []
    for w in span:
        if (w.ent_type > 0):
            res.append(w.ent_type_)
    return res


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


def main(model, text, id, tokens=False, debug=False):
    nlp = spacy.load(model)
    print("Loaded model '%s'" % model)

    # entities pipeline
    nlp.add_pipe(EntitiesPipeline(nlp), after='ner')

    # relations pipeline
    nlp.add_pipe(RelationPipeline(nlp), last=True)

    if (text):
        CORPUS = [{'text': text, 'relations': []}]
    elif is_spanish(model):
        CORPUS = CORPUS_ES
    else:
        CORPUS = CORPUS_EN

    if (id <= 0):
        print("Processing %d texts" % len(CORPUS))
    print()

    gold = Gold()
    num_docs_processed = 0
    show_warning = False
    for sample in CORPUS:
        doc_id = sample['id']
        if (id > 0 and id != doc_id):
            continue  # skip

        num_docs_processed += 1

        text = sample['text']
        print(text)
        doc = nlp(text)

        if (True == tokens):
            print()
            for t in doc:
                print('lemma: {}    pos: {}, dep: {}, ent_type: {}'
                      .format(t.lemma_, t.pos_, t.dep_, t.ent_type_))

        num_found = 0
        for r in doc._.relations:
            num_found += 1
            if (None != r.w):
                print('( {}/{}, {}, {}/{}, {} ), [{}]'
                      .format(r.s, ent_types(r.s), r.p, r.o, ent_types(r.o), r.w, r.x))
            else:
                print('( {}/{}, {}, {}/{} ), [{}]'
                      .format(r.s, ent_types(r.s), r.p, r.o, ent_types(r.o), r.x))

        if (0 == num_found):
            print('No relations!')

            if (len(doc.ents) == 0):
                print('No entities!')
            else:
                print('entities:')
                for e in doc.ents:
                    print('  {}/{}'.format(e.text, e.label_))

        # gold scoring for this document
        doc_scoring = gold.add(doc, doc_id, sample['relations'])
        if (None == doc_scoring):
            COLOR = bcolors.FAIL
            print('FAILED to get scoring for doc:', doc_id)
        else:
            COLOR = bcolors.DEFAULT

        if (doc_scoring.f1score() < 1.0):
            show_warning = True
            COLOR = bcolors.WARNING
        else:
            COLOR = bcolors.DEFAULT

        print(COLOR + 'doc-id: {} f1-score: {} (precision: {}, recall: {})'.format(
            doc_id, doc_scoring.f1score(), doc_scoring.precision(), doc_scoring.recall()))

        COLOR = bcolors.DEFAULT
        print(COLOR)

    if (num_docs_processed >= 2):
        if (show_warning):
            print(bcolors.WARNING + "some documents didn't pass!")
        else:
            print(bcolors.OKGREEN + 'all OK.')

        # print overall scoring
        overall_scoring = gold.scoring()
        print(bcolors.DEFAULT + '{} documents, overall scoring: f1-score: {} (precision: {}, recall: {})'.format(
            num_docs_processed, overall_scoring.f1score(), overall_scoring.precision(), overall_scoring.recall()))


if __name__ == '__main__':
    _argparser = argparse.ArgumentParser(
        description='test nlp-service entity extraction.')
    _argparser.add_argument('-i', '--id', type=int,
                            help='document id to process')
    _argparser.add_argument('-t', '--text', help='text to process')
    _argparser.add_argument('-m', '--model', help='model to use')
    _argparser.add_argument('--tokens', type=bool, nargs='?',
                            const=True, help='print token information')
    _argparser.add_argument('--debug', type=bool, nargs='?',
                            const=True, help='turn on debug mode')

    args = _argparser.parse_args()
    text = args.text if args.text else None
    model = args.model if args.model else __model
    id = args.id if args.id else -1
    tokens = True if args.tokens else False
    debug = True if args.debug else False

    main(model=model, text=text, id=id, tokens=tokens, debug=debug)
