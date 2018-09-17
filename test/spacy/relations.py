#!env/bin/python

'''
extract relations between entities
'''

from __future__ import unicode_literals, print_function

import spacy
import re

__model='en' # 'en'/'es'

__do_extract_is_relations = True
__do_extract_spo_relations = True
__do_extract_preposition_relations = True

TEXTS_EN = [
    'Hillary Clinton met secretly with Barak Obama last week.',
    'Donald Trump debate with Barak Obama and Hillary Clinton last Tuesday.',

    'Bill is the president of the U.S.',
    'Last week Hillary, mother of Chelsea, met with congressman Mike Pence in the White House.',
    'Mark Zuckerberg, CEO of Facebook, gave testimony in U.S. senate Sunday morning.',

    'Hillery killed David.',
    'David killed by Hillery.',

    'Hillery did not meet with Bill.',
    'Hillery is the biologic mother of Chelsea.',
    'Hillery is the step mother of Chelsea.',
    'Hillery is not the mother of Bill.',
]

TEXTS_ES = [
    'Hillary Clinton se reunió en secreto con Barack Obama la semana pasada.',
    'Donald Trump debate con Barack Obama y Hillary Clinton el martes pasado.',

    'Bill Clinton es el presidente de los EE. UU.',
    'La semana pasada, Hillery Clinton, madre de Chelsea Clinton, se reunió con el congresista Mike Pence en la Casa Blanca.',
    'Mark Zuckerberg, CEO de Facebook, dio su testimonio en el Senado de Estados Unidos el domingo por la mañana.',

    'Hillery Clinton mató a David',
    'David asesinado por Hillery Clinton',

    'Hillery Clinton no se encontró con Bill Clinton',
    'Hillery Clinton es la madre biológica de Chelsea Clinton',
    'Hillery Clinton es la madrastra de Chelsea Clinton',
    'Hillery Clinton no es la madre de Bill Clinton',
]

if (__model.startswith('es')):
    TEXTS = TEXTS_ES
else:
    TEXTS = TEXTS_EN

def is_subj(w):
    return None != re.match(r'[a-z]subj', w.dep_)

def is_compound(w):
    return w.dep_  == 'compound'

def is_root(w):
    return w.dep_ == 'ROOT'

def main(model='en'):
    nlp = spacy.load(model)
    print("Loaded model '%s'" % model)
    print("Processing %d texts" % len(TEXTS))
    print()

    print('text:')
    print('-----')
    for text in TEXTS:
        print(text)
    print()

    print('relations:')
    print('----------')
    for text in TEXTS:
        doc = nlp(text)
        relations = extract_relations(doc)
        for s, p, o in relations:
            print('({}, {}, {})'.format(s.text, p.text, o.text))

def extract_relations(doc):
    ''' extract relations between entities '''

    # merge entities into one token
    spans = list(doc.ents)
    for span in spans:
        span.merge()

    relations = []

    if (__do_extract_is_relations):
        extract_is_relations(doc, relations)
    if (__do_extract_spo_relations):
        extract_spo_relations(doc, relations)
    if (__do_extract_preposition_relations):
        extract_preposition_relations(doc, relations)
    
    relations = filter(lambda r: not is_neg(r), relations)
    return relations

def is_neg(r):
    _, p, _ = r
    rt = root(p)
    for w in rt.children:
        if (w.dep_ == 'neg'):
            return True
    return False

def root(w):
    if (type(w) == spacy.tokens.Span):
        head = w[0].head
    else:
        head = w.head

    while not is_root(head):
        head = head.head
    return head

def is_or_do_root(w):
    rt = root(w)
    if (rt.lemma_ == 'be' or rt.lemma_ == 'do'):
        return True
    return False

def extract_is_relations(doc, relations):
    ''' extract is/is_not relations '''
    subj_e_types = ['PERSON', 'PER', 'ORG']
    obj_e_types = ['PERSON', 'PER', 'ORG']
    
    for e in filter(lambda w: w.ent_type_ in subj_e_types, doc):
        if is_subj(e):
            if (is_or_do_root(e)):
                rt = root(e)
                pred_span = is_relation_pred_span_from_children(rt.children)
                for obj in extract_spo_objects(e, obj_e_types):
                    relations.append((e, pred_span, obj))

def is_relation_pred_span_from_children(children):
    pred = None
    filtered = filter(lambda w: w.dep_ == 'attr', children)
    list_ = list(filtered)
    if (len(list_) <= 0):
        return None
    pred = list_[-1] # last one
    i = pred.i
    for x in filter(lambda w: w.dep_ == 'compound', pred.lefts):
        i = min(x.i, i)
    pred_span =  pred.doc[i:pred.i+1]
    return pred_span

def extract_spo_relations(doc, relations):
    ''' extract (s,p,o) relations '''

    subj_e_types = ['PERSON', 'PER', 'ORG']
    obj_e_types = ['PERSON', 'PER', 'ORG']
    
    for e in filter(lambda w: w.ent_type_ in subj_e_types, doc):
        if is_subj(e) or is_compound(e) and is_root(e.head):
            pred = e.head

            if (is_or_do_root(pred)):
                continue # but not 'is mother of', 'is employee of', etc.

            # Hillery killed David vs. David killed by Hillery
            pred_rights = list(pred.rights)
            if (pred.pos_ == 'VERB'):
                for w in pred_rights:
                    if (w.dep_ in ('agent')):
                        pred = doc[pred.i : w.i+1]

            for e2 in extract_spo_objects(e, obj_e_types):
                relations.append((e, pred, e2)) # matched

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
                break # does not match (s,p,o) - missing (,p,) in between

            if (head2 == subj.head):
                # match
                obj_list.append(e2)
                break
            head2 = head2.head
    
    return obj_list

def extract_preposition_relations(doc, relations):
    ''' 
    extract (e1, preposition, e2) relations
    e.g: (s, mother_of, o), (s, employee_of, o)
    '''

    subj_types = ['PERSON', 'PER', 'ORG']
    obj_types = ['PERSON', 'PER', 'ORG']

    for pobj in filter(lambda w: w.ent_type_ in obj_types and w.dep_ in ('pobj'), doc):
        # 'mother of', 'employee of', etc.
        if (is_or_do_root(pobj)):
            continue # but not 'is mother of', 'is employee of', etc.

        if (pobj.head.dep_ == 'prep' and pobj.head.head.dep_ in ('appos', 'conj')):
            pred_span = doc[pobj.head.head.i : pobj.head.right_edge.i]
            first_subject = pobj.head.head.head
            subjects = [w for w in first_subject.subtree if w != pobj and w.ent_type_ in subj_types]
            for s in subjects:
                relations.append((s, pred_span, pobj)) # matched

if __name__ == '__main__':
    main(model=__model)

    # Expected output:
    # Net income      MONEY   $9.4 million
    # the prior year  MONEY   $2.7 million
    # Revenue         MONEY   twelve billion dollars
    # a loss          MONEY   1b
