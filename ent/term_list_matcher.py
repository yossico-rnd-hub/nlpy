import spacy
from spacy.tokens import Doc
from spacy.tokens import Span
from spacy.matcher import PhraseMatcher


class TermList_Matcher(object):
    '''
    match entities based on terminology list and an entity labels.
    '''

    name = 'term-list-ent-matcher'

    def __init__(self, nlp, term_list):
        self.matcher = PhraseMatcher(nlp.vocab)
        for item in term_list:
            label = item['label']
            terms = item['terms']
            patterns = [nlp(text) for text in terms]
            self.matcher.add(label, None, *patterns)

    def __call__(self, doc, entities):
        spans = []
        matches = self.matcher(doc)
        for label, start, end in matches:
            span = doc[start:end]
            if (span[0].ent_type == label):  # if not already labeled
                continue

            # es only: try extending the match (compound)
            compound_expanded = False
            # lilo
            # if (span.root.lang_ == 'es'):
            #     span = self._try_expand_compound(span, label)
            #     if (None != span):
            #         spans.append(span)
            #         compound_expanded = True

            if (False == compound_expanded):
                span = Span(doc, start, end, label=label)
                spans.append(span)

        if (len(spans) > 0):
            doc.ents = list(doc.ents) + spans
        return doc

    def _try_expand_compound(self, span, label):
        # try extending the match (compound)
        # either the match
        compound = span[0] if span[0].dep_ == 'compound' else None
        # or its children
        if (None == compound):
            compound = next(filter(lambda x: x.dep_ ==
                                   'compound', span[0].children), None)
        compound_start = compound_end = -1
        if (None != compound):
            # the entity starts from the head
            head = compound.head
            compound_start = compound_end = head.i
            for t in head.children:
                if (t.dep_ == 'compound'):
                    compound_start = min(compound_start, t.i)
                    compound_end = max(compound_end, t.i)

        if (compound_start >= 0):
            compound_span = Span(span.doc, compound_start,
                                 compound_end+1, label=label)
            return compound_span

        return None
