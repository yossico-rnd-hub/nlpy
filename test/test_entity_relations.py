#!env/bin/python

from __future__ import unicode_literals, print_function

import spacy

TEXTS = [
    'Hillary Clinton met with Barak Obama last week.',
    'Last week Hillary and Bill Clinton, parents of Chelsea, met secretly with Barak Obama at the White House.',
    'Mark Zuckerberg, CEO of Facebook, gave testimony in U.S. senate Sunday morning.',
    'Donald Trump debate with Barak Obama and Hillary Clinton last Tuesday.',
]

def main(model='en_core_web_sm'):
    nlp = spacy.load(model)
    print("Loaded model '%s'" % model)
    print("Processing %d texts" % len(TEXTS))
    print()

    for text in TEXTS:
        print(text)
    print()

    for text in TEXTS:
        doc = nlp(text)
        relations = extract_entity_relations(doc)
        for s, p, o in relations:
            print('({}, {}, {})'.format(s.text, p.text, o.text))

def extract_entity_relations(doc):
    ''' extract relations between entities '''

    # merge entities into one token
    spans = list(doc.ents)
    for span in spans:
        span.merge()

    relations = []

    extract_spo_relations(doc, relations)
    extract_preposition_relations(doc, relations)
    
    return relations

def extract_spo_relations(doc, relations):
    ''' extract (s,p,o) relations '''

    subj_e_types = ['PERSON', 'ORG']
    obj_e_types = ['PERSON', 'ORG']
    
    for e in filter(lambda w: w.ent_type_ in subj_e_types, doc):
        if e.dep_ in ('nsubj', 'compound') and e.head.dep_ == 'ROOT':
            for e2 in extract_spo_objects(e, obj_e_types):
                relations.append((e, e.head, e2)) # matched

def extract_spo_objects(subj, obj_e_types):
    ''' extract (s,p,o) objects '''
    obj_list = []
    for e2 in filter(lambda w: w.ent_type_ in obj_e_types, subj.sent):
        if (e2 == subj):
            continue # skip subj
        
        head2 = e2.head
        while (None != head2):
            if (head2 == subj):
                head2 = head2.head
                continue # does not match (s,p,o) - missing (,p,) in between

            if (head2 == subj.head):
                # match
                obj_list.append(e2)
                break
            head2 = head2.head
    
    return obj_list

def extract_preposition_relations(doc, relations):
    ''' 
    extract (e1, preposition, e2) relations
    e.g: mother_of, employee_of
    '''

    subj_types = ['PERSON', 'ORG']
    obj_types = ['PERSON', 'ORG']

    for pobj in filter(lambda w: w.ent_type_ in obj_types and w.dep_ in ('pobj'), doc):
        # 'mother of', 'employee of', etc.
        if (pobj.head.dep_ == 'prep' and pobj.head.head.dep_ == 'appos'):
            pred_span = doc[pobj.head.head.left_edge.i : pobj.head.right_edge.i]
            first_subject = pobj.head.head.head
            subjects = [w for w in first_subject.subtree if w != pobj and w.ent_type_ in subj_types]
            for s in subjects:
                relations.append((s, pred_span, pobj)) # matched

if __name__ == '__main__':
    main()

    # Expected output:
    # Net income      MONEY   $9.4 million
    # the prior year  MONEY   $2.7 million
    # Revenue         MONEY   twelve billion dollars
    # a loss          MONEY   1b
