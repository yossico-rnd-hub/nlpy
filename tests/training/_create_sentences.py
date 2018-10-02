#!../../env/bin/python

import spacy
import re

model = 'en'
nlp = spacy.load(model, disable=['parser', 'ner'])

# word = 'horse'
fname = 'horses'
word = 'cat'
fname = 'cats'

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

            escaped = sentence.replace("'", "\\'")
            escaped = escaped.replace("\"", "\\\"")

            f2.write(u'\t("{}", {{\n'.format(escaped))
            f2.write(u"\t\t'entities': [({}, {}, 'ANIMAL')]\n"
            .format(offset, length))
            f2.write(u"\t}),\n\n")
        f2.write(u"]")
