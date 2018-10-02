#!env/bin/python

import os
import logging
import argparse
import spacy
from spacy.gold import biluo_tags_from_offsets


def main(fname, label, model, debug=False):
    level = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(level=level, format='%(message)s')

    nlp = spacy.load(model)
    logging.info("Loaded model '%s'" % model)

    this_script_dir = os.path.dirname(os.path.abspath(__file__))

    _label = label

    _fname = os.path.join(this_script_dir, fname)
    _word = 'horse'

    # _fname = os.path.join(this_script_dir, 'cats')
    # _word = 'cat'

    # open input file
    with open(_fname) as f_in:
        # create output file (json-input-format)
        with open(_fname + '.train.json', 'w') as f_out:
            # start json-input-format
            f_out.write(u'[{\n')

            # convert input - line by line
            id = 0  # incremental doc-id
            for line in f_in:

                # skip irrelevant lines
                if len(line) < 10:
                    continue

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
                    if (t.orth_ == _word or t.lemma_ == _word):
                        entities.append((offset, offset+length, _label))
                    elif t.ent_type:
                        entities.append((offset, offset+length, t.ent_type_))
                biluo_tags = biluo_tags_from_offsets(doc, entities)

                # write json-input-format

                # ID of the document within the corpus
                f_out.write(u'\t"id": {},\n'.format(id))
                # list of paragraphs in the corpus
                f_out.write(u'\t"paragraphs": [{\n')
                # raw text of the paragraph
                # lilo: TODO - a better way?
                escaped = sentence.replace("'", "\\'")
                escaped = escaped.replace("\"", "\\\"")
                f_out.write(u'\t\t"raw": "{}",\n'.format(escaped))
                # list of sentences in the paragraph
                f_out.write(u'\t\t"sentences": [{\n')
                # list of tokens in the sentence
                f_out.write(u'\t\t\t"tokens": [{\n')

                for t in doc:
                    # index of the token in the document
                    f_out.write(u'\t\t\t\t"id": {},\n'.format(t.i))
                    # dependency label
                    f_out.write(u'\t\t\t\t"dep": "{}",\n'.format(t.dep_))
                    # offset of token head relative to token index
                    f_out.write(
                        u'\t\t\t\t"head": {},\n'.format(t.i - t.head.i))
                    # part-of-speech tag
                    f_out.write(u'\t\t\t\t"tag": "{}",\n'.format(t.tag_))
                    # verbatim text of the token
                    f_out.write(u'\t\t\t\t"orth": "{}",\n'.format(t.orth_))
                    # BILUO label, e.g. "O" or "U-ORG"
                    f_out.write(
                        u'\t\t\t\t"ner": "{}",\n'.format(biluo_tags[t.i]))

                # end tokens
                f_out.write(u'\t\t\t}],\n')
                # end sentence
                f_out.write(u'\t\t}],\n')
                # end paragraph
                f_out.write(u'\t}],\n')

            # end json-input-format
            f_out.write(u"}]")


if __name__ == '__main__':
    # process command-line args
    _argparser = argparse.ArgumentParser(
        description='conver a file line by line to spacy input-json-format.')

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
