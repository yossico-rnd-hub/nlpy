#!env/bin/python

import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc

# NER tags pure whitespace as entities #1717
# https://github.com/explosion/spaCy/issues/1717


def remove_whitespace_entities(doc):
    doc.ents = [e for e in doc.ents if not e.text.isspace()]
    return doc


nlp = spacy.load('en')
nlp.add_pipe(remove_whitespace_entities, after='ner')

matcher = Matcher(nlp.vocab)

# Get the ID of the 'EVENT' entity type. This is required to set an entity.
EVENT = nlp.vocab.strings['EVENT']

Doc.set_extension('prev_start', default=-1)
Doc.set_extension('prev_end', default=-1)


def add_event_ent(matcher, doc, i, matches):
    # Get the current match and create tuple of entity label, start and end.
    # Append entity to the doc's entity. (Don't overwrite doc.ents!)
    _, start, end = matches[i]

    # lilo:TODO - ommit overlapping matches
    if (i > 0):
        if (start >= doc._.prev_start and start <= doc._.prev_end):
            return None  # discard overlapping
    doc._.prev_start = start
    doc._.prev_end = end

    entity = (EVENT, start, end)
    doc.ents += (entity,)

    # print(doc[start:end].text, entity)


patterns = [
    [
        {'ENT_TYPE': 'ORG', 'OP': '+'},
        {'LIKE_NUM': False, 'OP': '+'},
        {'LIKE_NUM': True}
    ],
    [
        {'ENT_TYPE': 'ORG', 'OP': '+'},
        {'IS_ASCII': True, 'OP': '+'},
        {'ENT_TYPE': 'DATE', 'OP': '+'}
    ]
]

matcher.add('GoogleIO', add_event_ent, *patterns)

doc = nlp(
    u"This is a text about Google I/O 2015.\n"
    u"Another one is about Microsoft Xbox 2019.\n"
    u"IBM meetup November this year.\n"
)

# ---------------------------------------------------------
print(doc.text)
print()

# ---------------------------------------------------------
# print('tokens:')
# for token in doc:
#     print(token.text, '\tPOS: ', token.pos_, '\tlabel: ', token.ent_type_, '\ttag: ', token.tag_)
# print()

# ---------------------------------------------------------
# print('sentences:')
# for s in doc.sents:
#     print(s)
# print()

# ---------------------------------------------------------
# print('entities:')
matches = matcher(doc)
for e in doc.ents:
    print(e.start, e.end, '\t', e.label_, '\t', e.text)
