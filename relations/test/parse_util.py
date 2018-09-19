#!env/bin/python

'''
various utilities to help with relation extraction
'''

from __future__ import unicode_literals

import re


def is_xsubj(w):
    return None != re.match(r'[a-z]subj', w.dep_)


def is_root(w):
    return w.dep_ == 'ROOT'
