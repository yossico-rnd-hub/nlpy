#!env/bin/python

import os
import logging
import argparse
import random
import spacy
from spacy.gold import biluo_tags_from_offsets

from util import escape


def main(fname, label, model, debug=False):
    level = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(level=level, format='%(message)s')

    print("Loading model '%s' ... " % model)
    nlp = spacy.load(model)

    this_script_dir = os.path.dirname(os.path.abspath(__file__))

    _words = ['horse', ]
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

    # shuffle
    random.shuffle(lines)

    # dev/train split
    dev_length = len(lines) // 4
    split_list = [
        (lines[:dev_length], 'dev'),
        (lines[dev_length:], 'train'),
    ]

    # create output file (json-input-format)
    for lines, split_name in split_list:
        fname_out = '{}.{}.json'.format(_fname, split_name)
        print('generating spacy json-input-format: {} ...'.format(fname_out))
        with open(fname_out, 'w') as f_out:
            # start json-input-format
            f_out.write(u'[\n')

            # convert input - line by line
            id = 0  # incremental doc-id
            for line in lines:

                # line clenup
                sentence = line.strip('\r\n')

                # process sentence
                id += 1
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
                biluo_tags = biluo_tags_from_offsets(doc, entities)

                # write json-input-format

                # open doc
                if (id > 1):
                    f_out.write(u'\t,{\n')
                else:
                    f_out.write(u'\t{\n')

                # ID of the document within the corpus
                f_out.write(u'\t\t"id": {},\n'.format(id))

                # list of paragraphs in the corpus
                f_out.write(u'\t\t"paragraphs": [{\n')

                # raw text of the paragraph
                f_out.write(u'\t\t\t"raw": "{}",\n'.format(escape(sentence)))

                # list of sentences in the paragraph
                f_out.write(u'\t\t\t"sentences": [{\n')

                # list of tokens in the sentence
                f_out.write(u'\t\t\t\t"tokens": [\n')

                for t in doc:
                    # start token
                    if (t.i > 0):
                        f_out.write(u'\t\t\t\t\t,{ ')
                    else:
                        f_out.write(u'\t\t\t\t\t { ')
                    # index of the token in the document
                    f_out.write(u'"id": {}, '.format(t.i))
                    # dependency label
                    f_out.write(u'"dep": "{}", '.format(t.dep_))
                    # offset of token head relative to token index
                    f_out.write(
                        u'"head": {}, '.format(t.head.i - t.i))
                    # part-of-speech tag
                    f_out.write(u'"tag": "{}", '.format(t.tag_))
                    # verbatim text of the token
                    f_out.write(
                        u'"orth": "{}", '.format(escape(t.orth_)))
                    # BILUO label, e.g. "O" or "U-ORG"
                    f_out.write(
                        u'"ner": "{}" '.format(biluo_tags[t.i]))
                    # end token
                    f_out.write(u'}\n')  # without trailing ','

                # end tokens (sentence)
                f_out.write(u'\t\t\t\t]\n')

                # end sentences
                f_out.write(u'\t\t\t}]\n')

                # end paragraps
                f_out.write(u'\t\t}]\n')

                # end doc
                f_out.write(u'\t}\n')

            # end json-input-format
            f_out.write(u']\n')

    print('Done.')


if __name__ == '__main__':
    # process command-line args
    _argparser = argparse.ArgumentParser(
        description='convert a file to spacy input-json-format.')

    _argparser.add_argument('-f', '--file', type=str,
                            default='data/horses', help='input file')
    _argparser.add_argument('-l', '--label', type=str,
                            default='ANIMAL', help='label to use')
    _argparser.add_argument('-m', '--model', type=str,
                            default='en', help='model to use [en/es]')
    _argparser.add_argument('-d', '--debug', type=bool, default=False,
                            nargs='?', const=True, help='turn on debug mode')

    args = _argparser.parse_args()

    # call main
    main(fname=args.file, label=args.label, model=args.model, debug=args.debug)
