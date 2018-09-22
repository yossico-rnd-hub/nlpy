
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
