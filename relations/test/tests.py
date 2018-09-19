#!env/bin/python

'''
extract relations between entities
'''

import sys
sys.path.append('.')

import spacy
from spacy.tokens import Doc

from gold import Gold
from corpus_en import CORPUS_EN
from corpus_es import CORPUS_ES

from parse_util import is_root, is_xsubj

# from relations import *
from relations import RelationPipeline
from relations.lang.en import EN_SPO_RelationExtractor
from relations.lang.en import EN_IS_A_RelationExtractor
from relations.lang.es import ES_SPO_RelationExtractor

__model = 'en'  # 'en'/'es'


def is_spanish():
    return __model.startswith('es')


def is_english():
    return __model.startswith('en')


if is_spanish():
    CORPUS = CORPUS_ES

    __do_extract_is_relations = False
    __do_extract_spo_relations = True

    _subj_e_types = ['PER', 'ORG', 'MISC']
    _obj_e_types = ['PER', 'ORG', 'MISC']
else:
    CORPUS = CORPUS_EN

    __do_extract_is_relations = True
    __do_extract_spo_relations = True

    _subj_e_types = ['PERSON', 'ORG', 'GPE']
    _obj_e_types = ['PERSON', 'ORG', 'GPE']


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

    # extractors pipeline
    rel_pipeline = RelationPipeline()
    if is_spanish():
        rel_pipeline.add_pipe(ES_SPO_RelationExtractor())
    else:
        rel_pipeline.add_pipe(EN_SPO_RelationExtractor())
        rel_pipeline.add_pipe(EN_IS_A_RelationExtractor())

    show_warning = False
    for sample in CORPUS:

        text = sample['text']
        print(text)
        doc = nlp(text)

        # try to extract relations from all entity types available in the document
        types = list(set(e.label_ for e in doc.ents))
        _subj_e_types = types
        _obj_e_types = types

        extract_relations(doc)
        num_found = 0
        for s, p, o, w in doc._.relations:
            num_found += 1
            if (None != w):
                print('( {}/{}, {}, {}/{}, {} )'
                      .format(s.text, s.ent_type_, p.text, o.text, o.ent_type_, w.text))
            else:
                print('( {}/{}, {}, {}/{} )'
                      .format(s.text, s.ent_type_, p.text, o.text, o.ent_type_))

        if (0 == num_found):
            print('No relations!')

        # gold scoring for this document
        gold_relations = sample['relations']
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

    doc._.relations = list(filter(lambda r: not is_neg(r), relations))


def is_neg(r):
    _, p, _, _ = r
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
        if is_xsubj(e):
            if (is_or_do_root(e)):
                rt = root(e)
                pred_span = en_is_relation_pred_span_from_children(rt.children)
                for obj in en_extract_spo_objects(e, _obj_e_types):
                    relations.append((e, pred_span, obj, None))


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
        if ((is_xsubj(e)
             # {PERSON/compound} debate/noun with {PERSON/x}
             or (e.dep_ == 'compound'))
                and is_root(e.head)):

            pred = e.head

            en_extract_preposition_relations(e, doc, relations)  # lilo

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

            for obj in en_extract_spo_objects(e, _obj_e_types):
                # matched
                relations.append((e, pred, obj, en_extract_when(pred)))


def en_extract_when(pred):
    date_list = [w for w in pred.subtree if w.ent_type_ == 'DATE']
    when = date_list[0] if date_list else None
    if (None != when and when.dep_ == 'compound'):
        when = when.doc[min(when.i, when.head.i): max(when.i, when.head.i)+1]
    return when

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


# e.g: '... Hillery, mother of Chelsea, ...'
def en_extract_preposition_relations(e, doc, relations):
    '''
    extract (e1, preposition, e2) relations
    e.g: (... <nsubj>, mother of <pobj>, ...) or (... <nsubj>, employee of <pobj>, ...)
    '''
    pred = next(filter(lambda w: w.dep_ == 'appos', e.children), None)
    if (pred):
        prep = next(filter(lambda w: w.dep_ == 'prep', pred.rights), None)
        if (None != prep):
            pred_span = doc[pred.i: prep.i + 1]
        objects = [w for w in pred.subtree if w .dep_ in ('pobj', 'conj')]
        for obj in objects:
            r = (e, pred_span if pred_span else pred, obj, None)
            relations.append(r)


def es_extract_spo_relations(doc, relations):
    ''' extract (s,p,o) relations '''

    for e in filter(lambda w: w.ent_type_ in _subj_e_types, doc):
        if (is_xsubj(e)):
            pred = e.head
            obj = next(filter(
                lambda w: w != e and w.pos_ in ('NOUN', 'PROPN'), pred.children), None)
            if (None != obj):
                relations.append((e, pred, obj, None))  # matched
        elif (is_root(e)):
            pred = next(filter(
                lambda w: w != e and w.pos_ in ('VERB', 'NOUN', 'PROPN'), e.children), None)
            if (None != pred):
                obj = next(filter(
                    lambda w: w != e and w.pos_ in ('NOUN', 'PROPN'), pred.children), None)
                if (None != obj):
                    relations.append((e, pred, obj, None))  # matched


if __name__ == '__main__':
    main(model=__model)
