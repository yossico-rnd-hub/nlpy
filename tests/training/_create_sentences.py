#!env/bin/python

import os
import re
import spacy
from spacy.gold import biluo_tags_from_offsets


model = 'en'
nlp = spacy.load(model, disable=['parser', 'ner'])

_this_script_dir = os.path.dirname(os.path.abspath(__file__))
fname = os.path.join(_this_script_dir, 'horses')
word = 'horse'
# fname = os.path.join(_this_script_dir, 'cats')
# word = 'cat'

lines = []
with open(fname) as f:
    content = f.readlines()
    for line in content:
        if len(line) < 10:
            continue
        lines.append(line)
    with open(fname+'.py', 'w') as f2:
        f2.write(u"sentences = [\n")
        for sentence in lines:
            sentence = sentence.strip('\r\n')

            doc = nlp(sentence)
            offset = length = -1
            for t in doc:
                if t.lemma_ == word:
                    offset = t.idx
                    length = len(t.norm_)
                    break
            if offset < 0 or length <= 0:
                continue

            entities = [(offset, offset+length, 'ANIMAL')]
            tags = biluo_tags_from_offsets(doc, entities)
            assert tags == ['O', 'O', 'U-LOC', 'O']

            escaped = sentence.replace("'", "\\'")
            escaped = escaped.replace("\"", "\\\"")

            f2.write(u'\t("{}", {{\n'.format(escaped))
            f2.write(u"\t\t'entities': [({}, {}, 'ANIMAL')]\n"
                     .format(offset, length))
            f2.write(u"\t}),\n\n")
        f2.write(u"]")
