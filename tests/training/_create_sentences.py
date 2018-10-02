#!env/bin/python

import os
import re
import spacy
from spacy.gold import biluo_tags_from_offsets


model = 'en'
nlp = spacy.load(model, disable=['parser', 'ner'])

_this_script_dir = os.path.dirname(os.path.abspath(__file__))

_label = 'ANIMAL'

_fname = os.path.join(_this_script_dir, 'horses')
_word = 'horse'

# _fname = os.path.join(_this_script_dir, 'cats')
# _word = 'cat'

# open input file
with open(_fname) as f_in:
    # create output file
    with open(_fname + '.py', 'w') as f_out:

        # convert input - line by line
        for line in f_in:
            # skip irrelevant lines
            if len(line) < 10:
                continue

            # line clenup
            sentence = line.strip('\r\n')

            # process sentence
            doc = nlp(sentence)
            offset = length = -1
            for t in doc:
                if (t.orth_ == _word or t.lemma_ == _word):
                    offset = t.idx
                    length = len(t.lemma_)
                    break
            if offset < 0 or length <= 0:
                continue

            entities = [(offset, offset+length, _label)]
            tags = biluo_tags_from_offsets(doc, entities)

            escaped = sentence.replace("'", "\\'")
            escaped = escaped.replace("\"", "\\\"")

            f_out.write(u'\t("{}", {{\n'.format(escaped))
            f_out.write(u"\t\t'entities': [({}, {}, {})]\n"
                        .format(offset, length, _label))
            f_out.write(u"\t}),\n\n")
        f_out.write(u"]")
