#!env/bin/python

from __future__ import unicode_literals, print_function

import spacy

TEXTS = [
    # 'Hillary Clinton met with Barak Obama last week.',
    'Last week Hillary Clinton, mother of Chelsea, secretly met with Barak Obama at the White House.',
    'Today is Sunday.'
    'Donald Trump debate with Barak Obama and Hillary Clinton last Tuesday.',
]

def main(model='en_core_web_sm'):
    nlp = spacy.load(model)
    print("Loaded model '%s'" % model)
    print("Processing %d texts" % len(TEXTS))

    for text in TEXTS:
        doc = nlp(text)
        relations = extract_entity_relations(doc)
        for s, p, o in relations:
            print('({}, {}, {})'.format(s.text, p.text, o.text))


def extract_entity_relations(doc):
    # merge entities into one token
    spans = list(doc.ents)
    for span in spans:
        span.merge()

    relations = []
    subj_e_type = 'PERSON'
    obj_e_type = 'PERSON'
    for e in filter(lambda w: w.ent_type_ == subj_e_type, doc):
        if e.dep_ in ('nsubj', 'compound') and e.head.dep_ == 'ROOT':
            for e2 in extract_objects(e, obj_e_type):
                relations.append((e, e.head, e2)) # matched
    
    return relations

def extract_objects(e, obj_e_type):
    obj_list = []
    for e2 in filter(lambda w: w.ent_type_ == obj_e_type, e.sent):
        if (e2 == e):
            continue
        
        head2 = e2.head
        while (None != head2):
            if (head2 == e.head):
                # match
                obj_list.append(e2)
                break
            head2 = head2.head
    return obj_list

if __name__ == '__main__':
    main()

    # Expected output:
    # Net income      MONEY   $9.4 million
    # the prior year  MONEY   $2.7 million
    # Revenue         MONEY   twelve billion dollars
    # a loss          MONEY   1b
