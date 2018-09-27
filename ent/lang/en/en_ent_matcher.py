import spacy
from spacy.tokens import Doc
from spacy.tokens import Span
from spacy.matcher import PhraseMatcher

from .term_list import EN_TERM_LIST


class EN_TerminologyList_EntityMatcher(object):
    '''
    match entities based on terminology list and an entity labels.
    '''
    
    name = 'en_term_list_ent_matcher'

    def __init__(self, nlp):
        self.matcher = PhraseMatcher(nlp.vocab)
        for item in EN_TERM_LIST:
            label = item['label']
            terms = item['terms']
            patterns = [nlp(text) for text in terms]
            self.matcher.add(label, None, *patterns)

    def __call__(self, doc, entities):
        matches = self.matcher(doc)
        for match_id, start, end in matches:
            span = Span(doc, start, end, label=match_id)
            doc.ents = list(doc.ents) + [span]
        return doc
