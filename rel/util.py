
'''
various utilities to help with relation extraction
'''

import logging
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
    ''' return left conjunctions'''
    return list(filter(lambda w: w.dep_ == 'conj', span.lefts))


def _right_conj(w):
    ''' return right conjunctions'''
    return list(filter(lambda w: w.dep_ == 'conj', w.rights))


def extend_right(w, alist, dep):
    ''' e.g: for obl in extend_right(w, w.children, ('obl')): '''
    start = end = w.i
    for child in filter(lambda x: x.dep_ in dep, alist):
        start = min(start, child.i)
        end = max(end, child.i)
    return w.doc[start: end+1]


def _extend_compound(w):
    start = w.start if hasattr(w, 'start') else w.i
    end = w.end if hasattr(w, 'end') else w.i

    lang = root(w).lang_

    if ('en' == lang):
        # walk in reverse order on w.lefts
        # (congressman/NOUN/compound <- Mike/PROPN/compound <- Pence/PROPN)
        for left in filter(lambda t: t.dep_ in ('compound', 'amod'), reversed(list(w.lefts))):
            if (not left.pos_ == w.pos_):
                break
            start = min(start, left.i)
    elif ('es' == lang):
        for right in filter(lambda t: t.dep_ in ('compound', 'flat') and t.head == w, w.rights):
            end = max(end, right.i)

    return w.doc[start:end + 1]


def extract_when(pred_span):
    when = next(filter(
        lambda w: w.ent_type_ in ('DATE', 'TIME'), pred_span.subtree), None)

    if (None == when):
        pred_head = pred_span[0].head
        when = next(filter(
            lambda w: w.ent_type_ in ('DATE', 'TIME'), pred_head.children), None)

    if (None == when):
        return None

    if (when.dep_ in ('amod', 'compound')):
        return when.doc[when.i: when.head.i+1]  # extend right

    # lilo when_span = when.doc[when.i:when.i+1]
    when_span = extend_right(when, when.rights, ('amod'))

    return when_span


def create_relation(s, p, o):
    s = _extend_compound(s)
    o = _extend_compound(o)

    # if obj is DATE/TIME -> put in when component
    # e.g: Bill born 1977
    if (o[0].ent_type_ in ('DATE', 'TIME')):
        o = None  # lilo:return (s, p, None, o)

    w = extract_when(p)

    logging.debug('(x:util) when: {}'.format(w))

    return (s, p, o, w)
