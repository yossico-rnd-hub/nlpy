#!env/bin/python

import os
import logging
import argparse
import spacy

from util import escape


def main(fname, words, label, model, debug=False):
    level = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(level=level, format='%(message)s')

    print("Loading model '%s' ... " % model)
    nlp = spacy.load(model)

    this_script_dir = os.path.dirname(os.path.abspath(__file__))

    _words = list(map(lambda w: w.strip(), words.split(',')))
    _label = label

    # open input file
    _fname = os.path.join(this_script_dir, fname)
    print('reading from {} ...'.format(_fname))
    lines = []
    with open(_fname) as f_in:
        for line in f_in:
            # skip irrelevant lines
            if len(line) < 10:
                continue
            lines.append(line)

    # create output file
    fname_out = '{}.py'.format(_fname)
    with open(fname_out, 'w') as f_out:
        print('generating spacy BILUO format: {} ...'.format(fname_out))
        f_out.write(u"sentences = [\n")
        for line in lines:

            # line clenup
            sentence = line.strip('\r\n')

            # process sentence
            doc = nlp(sentence)

            # perpare BILUO tags
            entities = []
            for t in doc:
                offset = t.idx
                length = len(t.lemma_)
                if (t.orth_ in _words or t.lemma_ in _words):
                    entities.append((offset, offset+length, _label))
                elif t.ent_type:
                    entities.append((offset, offset+length, t.ent_type_))

            f_out.write(u'\t("{}", {{\n'.format(escape(sentence)))
            f_out.write(u'\t\t"entities": {}\n'.format(entities))
            f_out.write(u"\t}),\n\n")
        f_out.write(u"]")


if __name__ == '__main__':
    # process command-line args
    _argparser = argparse.ArgumentParser(
        description='convert a file to spacy BILUO format.')

    _argparser.add_argument('-f', '--file', type=str,
                            default='data/horses', help='input file')
    _argparser.add_argument('-w', '--words', type=str,
                            default='cat, horse', help='words to label')
    _argparser.add_argument('-l', '--label', type=str,
                            default='ANIMAL', help='label to use')
    _argparser.add_argument('-m', '--model', type=str,
                            default='en', help='model to use [en/es]')
    _argparser.add_argument('-d', '--debug', type=bool, default=False,
                            nargs='?', const=True, help='turn on debug mode')

    args = _argparser.parse_args()

    # call main
    main(fname=args.file, words=args.words, label=args.label,
         model=args.model, debug=args.debug)
