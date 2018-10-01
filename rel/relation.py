import spacy
from spacy.tokens import Token, Span, Doc

_USE_SIMILARITY_MATCH = True


def str_match(nlp, s1, s2):
    if (_USE_SIMILARITY_MATCH):
        return str_match_similarity(nlp, s1, s2)
    if (txt(s1) != txt(s2)):
        return False
    return True


def txt(x):
    if isinstance(x, str):
        return x
    if (x and isinstance(x, Token) or isinstance(x, Span)):
        return x.text
    return None


def str_match_similarity(nlp, s1, s2):
    if (None != s1 and None != s2):
        span1 = to_span(nlp, s1)
        span2 = to_span(nlp, s2)
        sim = span1.similarity(span2)
        if (sim >= 0.5):
            return True
    if (None == s1 and None == s2):
        return True
    return False


def to_span(nlp, x):
    if isinstance(x, Span):
        return x
    if isinstance(x, Token):
        return x.doc[x.i, x.i+1]
    if isinstance(x, str):
        # lilo: doc = nlp(x)
        with nlp.disable_pipes('ws_relations'):
            doc = nlp(x)
        return doc[doc[0].i:doc[-1].i+1]
    return None


class Relations(object):

    ''' a for enumerating relation collection '''

    def __init__(self, nlp):
        self._relations = []
        self.nlp = nlp

    def __iter__(self):
        return iter(self._relations)

    def __len__(self):
        return len(self._relations)

    def __getitem__(self, index):
        return self._relations[index]

    def __iadd__(self, other):
        if (isinstance(other, Relations)):
            self._relations += other._relations
            return self

        if (isinstance(other, list)):
            self._relations += other
            return self

        if (isinstance(other, Relation)):
            self._relations.append(other)
            return self

        msg = "'%s' object can't be concatenated!" % type(other).__name__
        raise TypeError(msg)

    def append(self, r):
        if (isinstance(r, Relation)):
            self._relations.append(r)
            return
        if (isinstance(r, tuple)):
            s, p, o, w = r
            self._relations.append(Relation(s, p, o, w))
            return

        msg = "'%s' object can't be appended!" % type(r).__name__
        raise TypeError(msg)

    def remove(self, r):
        self._relations.remove(r)

    def contains(self, r):
        for _r in self:
            if not str_match(self.nlp, _r.s, r.s):
                continue
            if not str_match(self.nlp, _r.p, r.p):
                continue
            if not str_match(self.nlp, _r.o, r.o):
                continue
            if not str_match(self.nlp, _r.w, r.w):
                continue
            return True

        return False


class Relation(object):
    ''' a single relation represents (subject, predicate, object, when) '''

    def __init__(self, s, p, o, w=None, x=None):
        '''
        s: subject \n
        p: predicate \n
        o: object \n
        w: when \n
        x: originating extractor
        '''

        self.s = s
        self.p = p
        self.o = o
        self.w = w
        self.x = x

    def __str__(self):
        return str((self.s, self.o, self.p, self.w))

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()
