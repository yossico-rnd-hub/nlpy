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
        ent_spans = []
        found_split = False
        for e in doc.ents:
            if (e.end - e.start > 1):  # more than a single token?
                start = end = -1
                for t in e:
                    if (t.text == 'y'):
                        if (start >= 0 and end >= 0):
                            # lilo:remove label of 'y'
                            span = Span(doc, t.i, t.i+1, label=0)
                            ent_spans.append(span)
                            span = Span(doc, start, end+1, label=e.label)
                            ent_spans.append(span)
                            start = end = -1
                            if (not found_split):
                                found_split = True
                    else:
                        if (start < 0):
                            start = t.i
                        end = t.i

                if (start >= 0 and end >= 0):
                    span = Span(doc, start, end+1, label=e.label)
                    ent_spans.append(span)

        if (found_split and len(ent_spans) > 0):
            doc.ents = list(doc.ents) + ent_spans
        return doc
