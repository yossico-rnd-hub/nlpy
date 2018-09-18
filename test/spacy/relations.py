#!env/bin/python

'''
extract relations between entities
'''

from __future__ import unicode_literals, print_function

import spacy
from spacy.tokens import Doc
import re

__model = 'en'  # 'en'/'es'


def is_spanish():
    return __model.startswith('es')


def is_english():
    return __model.startswith('en')


if is_spanish():
    __do_extract_is_relations = False
    __do_extract_spo_relations = True
    __do_extract_preposition_relations = False

    _subj_e_types = ['PER', 'ORG', 'MISC']
    _obj_e_types = ['PER', 'ORG', 'MISC']
else:
    __do_extract_is_relations = True
    __do_extract_spo_relations = True
    __do_extract_preposition_relations = True

    _subj_e_types = ['PERSON', 'ORG', 'GPE']
    _obj_e_types = ['PERSON', 'ORG', 'GPE']

CORPUS_EN = [
    {'text': 'Hillary Clinton met secretly with Barak Obama last week.',
        'relations': [('Hillary Clinton', 'met', 'Barak Obama')]},
    {'text': 'Donald Trump debate with Barak Obama and Hillary Clinton last Tuesday.',
        'relations': [('Donald Trump', 'debate', 'Barak Obama'),
                      ('Donald Trump', 'debate', 'Hillary Clinton')]},

    {'text': 'Bill is the president of the U.S.',
        'relations': [('Bill', 'president', 'U.S.')]},
    {'text': 'Last week Hillary, mother of Chelsea, met with congressman Mike Pence in the White House.',
        'relations': [('Hillary', 'met', 'Mike Pence'),
                      ('Hillary', 'mother of', 'Chelsea')]},
    {'text': 'Mark Zuckerberg, CEO of Facebook, gave testimony to the U.S. Senate Sunday morning.',
        'relations': [('Mark Zuckerberg', 'gave testimony', 'the U.S. Senate'),
                      ('Mark Zuckerberg', 'CEO of', 'Facebook')]},

    {'text': 'Hillery killed David.',
        'relations': [('Hillery', 'killed', 'David')]},
    {'text': 'David killed by Hillery.',
        'relations': [('David', 'killed by', 'Hillery')]},

    {'text': 'Hillery did not meet with Bill.',
        'relations': []},
    {'text': 'Hillery is the biologic mother of Chelsea.',
        'relations': [('Hillery', 'mother', 'Chelsea')]},
    {'text': 'Hillery is the step mother of Chelsea.',
        'relations': [('Hillery', 'step mother', 'Chelsea')]},
    {'text': 'Hillery is not the mother of Bill.',
        'relations': []},
]

CORPUS_ES = [
    # OK
    {'text': 'Hillary Clinton se reunió en secreto con Barack Obama la semana pasada.',
        'relations': [('Hillary Clinton', 'reunió', 'Barack Obama')]},
    {'text': 'Donald Trump debate con Barack Obama y Hillary Clinton el martes pasado.',
        'relations': [('Donald Trump', 'debate', 'Barack Obama')]},

    {'text': 'Bill Clinton es el presidente de los U.S.A',
        'relations': [('Bill Clinton', 'presidente', 'U.S.A')]},

    # FIX
    # 'Last week Hillary, mother of Chelsea, met with congressman Mike Pence in the White House.'
    # {'text': 'La semana pasada, Hillery Clinton, madre de Chelsea Clinton, se reunió con el congresista Mike Pence en la Casa Blanca.',
    #     'relations': [('Hillary Clinton', 'conoció', 'Mike Pence'),
    #                   ('Hillary Clinton', 'madre de', 'Chelsea Clinton')]},
    
    # FIX(*)
    # 'Mark Zuckerberg, CEO de Facebook, dio su testimonio al Senado de los Estados Unidos el domingo por la mañana.',
    # OK
    # 'Bill Gates, CEO de Microsoft.'
    # 'Mark Zuckerberg es el CEO de Facebook.'

    # FIX(Hillery Clinton -> Hillery)
    # 'Hillery Clinton mató a David',
    # FIX(*)
    # 'David asesinado por Hillery Clinton',

    # FIX
    # 'Hillery Clinton no se encontró con Bill Clinton',
    # 'Hillery Clinton es la madre biológica de Chelsea Clinton',
    # 'Hillery Clinton es la madrastra de Chelsea Clinton',
    # 'Hillery Clinton no es la madre de Bill Clinton',
]

if (is_spanish()):
    CORPUS = CORPUS_ES
else:
    CORPUS = CORPUS_EN


def is_subj(w):
    return None != re.match(r'[a-z]subj', w.dep_)


def is_compound(w):
    return w.dep_ == 'compound'


def is_root(w):
    return w.dep_ == 'ROOT'


class Gold(object):
    def __init__(self, doc, gold_relations):
        doc_relations = list(
            map(lambda r: self.relation_to_string_tuple(r), doc._.relations))

        if (len(doc_relations) == 0 and len(gold_relations) == 0):
            # empty match
            self.precision = 1.0
            self.recall = 1.0
            self.f1score = 1.0
            return

        true_positives = 0
        false_positives = 0
        false_negatives = 0

        for r in doc_relations:
            if (r in gold_relations):
                true_positives += 1
            else:
                false_positives += 1

        for r in gold_relations:
            if (r not in doc_relations):
                false_negatives += 1

        precision = true_positives / (true_positives + false_positives) \
            if (true_positives + false_positives > 0) else 0.0
        recall = true_positives / (true_positives + false_negatives) \
            if (true_positives + false_negatives > 0) else 0.0
        f1score = 2 * (precision * recall) / (precision + recall) \
            if (precision + recall > 0) else 0.0

        self.precision = precision
        self.recall = recall
        self.f1score = f1score

    def relation_to_string_tuple(self, r):
        s, p, o = r
        return (s.text, p.text, o.text)

    def match_rel(self, r, gold_r):
        if (None == r and None != gold_r):
            return False
        if (None != r and None == gold_r):
            return False

        s, p, o = r
        gs, gp, go = gold_r

        if (s != gs):
            return False
        if (p != gp):
            return False
        if (o != go):
            return False

        return True


class bcolors:
    DEFAULT = '\033[0m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main(model='en'):
    nlp = spacy.load(model)
    print("Loaded model '%s'" % model)
    print("Processing %d texts" % len(CORPUS))
    print()

    Doc.set_extension('relations', default=[])

    show_warning = False
    for sample in CORPUS:
        text = sample['text']
        gold_relations = sample['relations']

        print(text)
        doc = nlp(text)

        # try to extract relations from all entity types available in the document
        types = list(set(e.label_ for e in doc.ents))
        _subj_e_types = types
        _obj_e_types = types

        extract_relations(doc)
        num_found = 0
        for s, p, o in doc._.relations:
            num_found += 1
            print('( {}/{}, {}, {}/{} )'
                  .format(s.text, s.ent_type_, p.text, o.text, o.ent_type_))

        if (0 == num_found):
            print('No relations!')

        # gold scoring for this document
        gold = Gold(doc, gold_relations)

        if (gold.f1score < 1.0):
            show_warning = True
            COLOR = bcolors.WARNING
        else:
            COLOR = bcolors.DEFAULT

        print(COLOR + 'f1score: {} (precision: {}, recall: {})'.format(
            gold.f1score, gold.precision, gold.recall))

        COLOR = bcolors.DEFAULT
        print(COLOR)

    if (len(CORPUS) >= 2):
        if (show_warning):
            print(bcolors.WARNING + "some didn't pass!")
        else:
            print(bcolors.OKGREEN + 'all OK.')


def extract_relations(doc):
    ''' extract relations between entities '''

    # merge entities into one token
    spans = list(doc.ents)
    for span in spans:
        span.merge()

    relations = []

    if (__do_extract_is_relations):
        en_extract_is_relations(doc, relations)
    if (__do_extract_spo_relations):
        if (is_english()):
            en_extract_spo_relations(doc, relations)
        elif (is_spanish()):
            es_extract_spo_relations(doc, relations)
    if (__do_extract_preposition_relations):
        en_extract_preposition_relations(doc, relations)

    doc._.relations = list(filter(lambda r: not is_neg(r), relations))


def is_neg(r):
    _, p, _ = r
    rt = root(p)
    for w in rt.children:
        if (w.dep_ == 'neg'):
            return True
    return False


def root(w):
    if (type(w) == spacy.tokens.Span):
        head = w[0].head
    else:
        head = w.head

    while not is_root(head):
        head = head.head
    return head


def is_or_do_root(w):
    rt = root(w)
    if (rt.lemma_ == 'be' or rt.lemma_ == 'do'):
        return True
    return False


def en_extract_is_relations(doc, relations):
    ''' extract is/is_not relations '''

    for e in filter(lambda w: w.ent_type_ in _subj_e_types, doc):
        if is_subj(e):
            if (is_or_do_root(e)):
                rt = root(e)
                pred_span = en_is_relation_pred_span_from_children(rt.children)
                for obj in en_extract_spo_objects(e, _obj_e_types):
                    relations.append((e, pred_span, obj))


def en_is_relation_pred_span_from_children(children):
    pred = None
    filtered = filter(lambda w: w.dep_ == 'attr', children)
    list_ = list(filtered)
    if (len(list_) <= 0):
        return None
    pred = list_[-1]  # last one
    i = pred.i
    for x in filter(lambda w: w.dep_ == 'compound', pred.lefts):
        i = min(x.i, i)
    pred_span = pred.doc[i:pred.i+1]
    return pred_span


def en_extract_spo_relations(doc, relations):
    ''' extract (s,p,o) relations '''

    for e in filter(lambda w: w.ent_type_ in _subj_e_types, doc):
        if ((is_subj(e)
             or is_compound(e))  # {PERSON/compound} debate/noun with {PERSON/x}
                and is_root(e.head)):
            pred = e.head

            if (is_or_do_root(pred)):
                continue  # but not 'is mother of', 'is employee of', etc.

            # e.g: 'killed by', 'gave testimony', etc. (but not 'killed Bill')
            pred_rights = list(pred.rights)
            if (pred.pos_ == 'VERB'):
                for w in pred_rights:
                    if (w.ent_type > 0):
                        continue  # do NOT merge with pred
                    if (w.dep_ in ('agent', 'dobj')):
                        pred = doc[pred.i: w.i+1]  # merge with pred

            for e2 in en_extract_spo_objects(e, _obj_e_types):
                relations.append((e, pred, e2))  # matched


# lilo:TODO - conj -> multiple objects (also multiple subjects)
#   '{Donald/compound} {Trump/compound} {debate/ROOT} {with/prep} {Barak/compound} {Obama/pobj} and {Hillary/compound} {Clinton/conj} last Tuesday.'
def en_extract_spo_objects(subj, _obj_e_types):
    ''' extract (s,p,o) objects '''
    obj_list = []
    for e2 in filter(lambda w: w.ent_type_ in _obj_e_types, subj.sent):
        if (e2 == subj):
            continue  # skip subj

        head2 = e2.head
        while (None != head2):
            if (head2 == subj):
                head2 = head2.head
                break  # does not match (s,p,o) - missing (,p,) in between

            if (head2 == subj.head):
                # match
                obj_list.append(e2)
                break
            head2 = head2.head

    return obj_list


def en_extract_preposition_relations(doc, relations):
    '''
    extract (e1, preposition, e2) relations
    e.g: (s, mother_of, o), (s, employee_of, o)
    '''

    subj_types = ['PERSON', 'PER', 'ORG']
    obj_types = ['PERSON', 'PER', 'ORG']

    for pobj in filter(lambda w: w.ent_type_ in obj_types and w.dep_ in ('pobj'), doc):
        # 'mother of', 'employee of', etc.
        if (is_or_do_root(pobj)):
            continue  # but not 'is mother of', 'is employee of', etc.

        if (pobj.head.dep_ == 'prep' and pobj.head.head.dep_ in ('appos', 'conj')):
            pred_span = doc[pobj.head.head.i: pobj.head.right_edge.i]
            first_subject = pobj.head.head.head
            subjects = [w for w in first_subject.subtree if w !=
                        pobj and w.ent_type_ in subj_types]
            for s in subjects:
                relations.append((s, pred_span, pobj))  # matched


def es_extract_spo_relations(doc, relations):
    ''' extract (s,p,o) relations '''

    for e in filter(lambda w: w.ent_type_ in _subj_e_types, doc):
        if (is_subj(e)):
            pred = e.head
            obj = next(filter(
                lambda w: w != e and w.pos_ in ('NOUN', 'PROPN'), pred.children), None)
            if (None != obj):
                relations.append((e, pred, obj))  # matched
        elif (is_root(e)):
            pred = next(filter(
                lambda w: w != e and w.pos_ in ('VERB', 'NOUN', 'PROPN'), e.children), None)
            if (None != pred):
                obj = next(filter(
                    lambda w: w != e and w.pos_ in ('NOUN', 'PROPN'), pred.children), None)
                if (None != obj):
                    relations.append((e, pred, obj))  # matched


if __name__ == '__main__':
    main(model=__model)

    # Expected output:
    # Net income      MONEY   $9.4 million
    # the prior year  MONEY   $2.7 million
    # Revenue         MONEY   twelve billion dollars
    # a loss          MONEY   1b
