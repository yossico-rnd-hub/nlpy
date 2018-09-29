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
        ents = []
        splited_ents = []
        found_split = False
        for e in doc.ents:
            split_token = next(filter(lambda t: t.text == 'y', e), None)
            if (None == split_token):
                ents.append(e)  # include entity as is
            else:
                # entity contains split_token
                if (e.end - e.start > 1):  # more than a single token?
                    found_split = True
                    start = end = -1
                    for t in e:
                        if (t.text == 'y'):
                            if (start >= 0 and end >= 0):
                                splited_ents.append(
                                    Span(doc, start, end+1, label=e.label))
                                start = end = -1
                        else:
                            if (start < 0):
                                start = t.i
                            end = t.i

                    if (start >= 0 and end >= 0):
                        splited_ents.append(
                            Span(doc, start, end+1, label=e.label))

        if (found_split):
            doc.ents = ents + splited_ents
            print('----------------------------------')
            print(doc.ents)
            print('----------------------------------')
        return doc
