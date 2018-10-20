class Span(object):
    def __init__(self, text='', start_char=-1, end_char=-1):
        self.text = text
        self.start_char = start_char
        self.end_char = end_char

class Entity(Span):
    def __init__(self, text='', start_char=-1, end_char=-1, label=''):
        super().__init__(text, start_char, end_char)
        self.label = label


class Relation(object):
    def __init__(self, s, p, o, w):
        self.s = s
        self.p = p
        self.o = o
        self.w = w

class Document(object):
    def __init__(self, text=''):
        self.text = text
        self.entities = []
        self.relations = []
