#!env/bin/python

import sys
sys.path.append('.')

import logging
import argparse
import timeit
from nlp import Nlpy
from gold import Gold
from corpus_en import CORPUS_EN
from corpus_es import CORPUS_ES
'''
test extracting entity relations
'''

global _DEBUG


def is_spanish(model):
    return model.startswith('es')


def ent_types(span):
    ''' returns an array of entity-types for each token in the span'''
    return span[0].ent_type_ if span else None


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


def main(model, id, text, tokens=False, debug=False):
    level = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(level=level, format='%(message)s')

    if text:
        CORPUS = [{'id': 1, 'text': text, 'relations': []}]
    elif is_spanish(model):
        CORPUS = CORPUS_ES
    else:
        CORPUS = CORPUS_EN

    if (id <= 0):
        print("Processing %d texts" % len(CORPUS))
    print()

    # start time
    start = timeit.default_timer()

    nlp = Nlpy.load(model)
    gold = Gold(nlp)
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
            print('{:20}\t{:10}\t{:10}\t{:10}'.format(
                'NORM', 'POS', 'DEP', 'LABEL'))
            print()
            for t in doc:
                print('{:20}\t{:10}\t{:10}\t{:10}'.format(
                    t.norm_, t.pos_, t.dep_, t.ent_type_))
            print()

        num_found = 0
        for r in doc._.relations:
            num_found += 1
            if r.w:
                print('({} / {}, {}, {} / {}, {}) [x: {}]'
                      .format(r.s, ent_types(r.s), r.p, r.o, ent_types(r.o), r.w, r.x))
            else:
                print('({} / {}, {}, {} / {}) [x: {}]'
                      .format(r.s, ent_types(r.s), r.p, r.o, ent_types(r.o), r.x))

        if (0 == num_found):
            print('No relations!')

            if (True == debug):
                _DEBUG = True
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

    # print summary if processing more than 1 document
    if (num_docs_processed >= 2):
        if (show_warning):
            print(bcolors.WARNING + "some documents didn't pass!")
        else:
            print(bcolors.OKGREEN + 'all OK.')
        # print overall scoring
        overall_scoring = gold.scoring()
        print(bcolors.DEFAULT + '{} documents, overall scoring: f1-score: {} (precision: {}, recall: {})'.format(
            num_docs_processed, overall_scoring.f1score(), overall_scoring.precision(), overall_scoring.recall()))
        print('timeit: {0:.2f} sec'.format(timeit.default_timer() - start))


if __name__ == '__main__':
    # process command-line args
    _argparser = argparse.ArgumentParser(
        description='test entity relation extraction.')

    _argparser.add_argument('-m', '--model', type=str,
                            default='en', help='model to use [en/es]')
    _argparser.add_argument('-i', '--id', type=int,
                            default=-1, help='document id to process')
    _argparser.add_argument('-t', '--text', type=str,
                            default=None, help='text to process')
    _argparser.add_argument('--tokens', type=bool, default=False,
                            nargs='?', const=True, help='print token information')
    _argparser.add_argument('-d', '--debug', type=bool, default=False,
                            nargs='?', const=True, help='turn on debug mode')

    args = _argparser.parse_args()

    # call main
    main(model=args.model, id=args.id, text=args.text,
         tokens=args.tokens, debug=args.debug)
