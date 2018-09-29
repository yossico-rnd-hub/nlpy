import logging
import spacy
from spacy.tokens import Span


class ES_EntitySplit(object):
    '''
    split entities based on rules
    e.g: 'Bill y Hillary Clinton' => 'Bill' + 'Hillary Clinton' (and remove label from 'y')
    '''

    name = 'es-ent-split'

    def __init__(self):
        pass

    def __call__(self, doc, entities):
        ents_splited = []
        ents_not_modified = []
        for e in doc.ents:
            if (len(e) < 3):
                # include entity as is
                ents_not_modified.append(e)
                continue

            # search for split_token
            split_token = next(filter(lambda t: t.text == 'y', e), None)
            if (None == split_token):
                # include entity as is
                ents_not_modified.append(e)
                continue

            # entity contains split_token
            for span in self.split_entity(e, split_token):
                ents_splited.append(span)

        if (len(ents_splited) > 0):
            # debug print before
            logging.debug('x:{} (doc.ents before): {}'.format(
                self.name, doc.ents))

            # update doc.ents
            doc.ents = ents_not_modified + ents_splited

            # debug print after
            logging.debug('x:{} (doc.ents after): {}'.format(
                self.name, doc.ents))

        return doc

    def split_entity(self, e, split_token):
        ''' split entity(e) on token(t) '''
        spans = []
        start = e.start
        for t in e:
            if (t.lemma == split_token.lemma):
                # create a span from start upto splitting token
                spans.append(Span(e.doc, start, t.i, label=e.label))
                # update start just after splitting token
                start = t.i + 1
            elif (t.i == e[-1].i):
                # append last entity token
                spans.append(Span(e.doc, start, t.i+1, label=e.label))

        return spans
