
'''
various utilities to help with relation extraction
'''

# from __future__ import unicode_literals

import re
import spacy


def is_xsubj(w):
    return None != re.match(r'[a-z]subj', w.dep_)


def is_root(w):
    return w.dep_ == 'ROOT'


def root(w):
    if (type(w) == spacy.tokens.Span):
        head = w[0].head
    else:
        head = w.head

    while not is_root(head):
        head = head.head
    return head


def _extend_lefts(w):
    start = end = w.i
    for left in filter(lambda t: t.pos_ == w.pos_ or t.dep_ in ('compound', 'amod'), w.lefts):
        start = left.i
    return w.doc[start:end + 1]


def _left_conj(span):
    ''' yield span and any left conjunctions'''
    res = [span]
    for conj in filter(lambda w: w.dep_ == 'conj', span.lefts):
        res.append(_extend_entity_name(conj))
    return res


def _right_conj(span):
    ''' yield span and any right conjunctions'''
    res = [span]
    for conj in filter(lambda w: w.dep_ == 'conj', span.rights):
        res.append(_extend_entity_name(conj))
    return res


def is_neg(v):
    for w in v.lefts:
        if (w.dep_ == 'neg'):
            return True
    return False


def _extend_entity_name(w):
    start = end = w.i

    # en:
    # walk in reverse order on w.lefts 
    # (congressman/NOUN/compound <- Mike/PROPN/compound <- Pence/PROPN)
    for left in filter(lambda t: t.dep_ in ('compound', 'amod'), reversed(list(w.lefts))):
        if (not left.pos_ == w.pos_):
            break
        start = min(start, left.i)

    # es:
    if (start == end):
        for right in filter(lambda t: t.dep_ in ('flat') and t.head == w, w.rights):
            end = max(end, right.i)

    return w.doc[start:end + 1]
