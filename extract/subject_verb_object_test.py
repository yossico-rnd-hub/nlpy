#!env/bin/python

import sys
sys.path.append('.')

import spacy

# import extract
from extract import subject_verb_object, extract_when

# nlp = spacy.load('es')
# TEXTS = [
#     u'Hillary Clinton se reunió en secreto con Barack Obama la semana pasada.',
#     u'Donald Trump tuvo un debate con Barack Obama y Hillary Clinton el martes pasado.',
# ]

nlp = spacy.load('en')
TEXTS = [
    u'When Sebastian Thrun started working on self-driving cars at '
    u'Google in 2007, few people outside of the company took him '
    u'seriously. “I can tell you very senior CEOs of major American '
    u'car companies would shake my hand and turn away because I wasn’t '
    u'worth talking to,” said Thrun, now the co-founder and CEO of '
    u'online higher education startup Udacity, in an interview with '
    u'Recode earlier this week.',

    u'Donald Trump had a debate with Barak Obama and Hillary Clinton last Tuesday.',
    u'Last week Hillary, mother of Chelsea and Dan, met with congressman Mike Pence in the White House.',
    u'Mark Zuckerberg, CEO of Facebook, gave testimony to the U.S. Senate Sunday morning.',

    u'Hillary Clinton met secretly with Barak Obama last week.',
    u'Hillery killed David.',
    u'David killed by Hillery.',
    u'Bill is the president of the U.S.',
    u'George Washington was the first president of the U.S.',
    u'Hillery is the biologic mother of Chelsea.',
    u'Hillery is the step mother of Chelsea.',
    u'Hillery did not meet with Bill.',
]

for text in TEXTS:
    doc = nlp(text)
    print(text)
    num_res = 0
    for t in subject_verb_object(doc,
                                 exclude_negation=True,
                                 entities_only=True):
        s, v, o = t
        when = extract_when(v)
        print((s, v, o, when) if when else t)
        num_res += 1
    if (0 == num_res):
        print('no triples!')
    print()
