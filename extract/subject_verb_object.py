

def subject_verb_object(doc,
                        exclude_negation=True,
                        entities_only=True):
    ''' extract (subject, verb, object) triples '''

    for s in filter(lambda t: t.dep_ in ('nsubj'), doc):
        if (entities_only and 0 == s.ent_type):
            continue  # skip none-entity
        subj = _extend_lefts(s)
        # print('lilo - subj:', subj)
        verb = _extract_verb(s, entities_only)
        # print('lilo - verb:', verb)
        if (None != verb):
            for obj in _extract_objects(verb, entities_only):
                # print('lilo - obj:', obj)
                if (not exclude_negation or not is_neg(verb)):
                    yield (subj, verb, obj)


def _extract_verb(s, entities_only=True):
    ''' try to extract the VERB related to the given subject '''
    if (s.head.pos_ != 'VERB'):
        return None

    verb = s.head

    # verb expansion rules

    # rule 1: '... <started/advcl> <-> <working/xcomp> at Google...'
    if (verb.dep_ == 'advcl'):
        right_verb = next(
            filter(lambda w: w.pos_ == 'VERB' and w.dep_ == 'xcomp', verb.rights), None)
        if (None != right_verb):
            return verb.doc[verb.i: right_verb.i+1]

    # rule 2: <PERSON/nsubj> <killed/VERB> <by/agent> <PERSON/pobj>
    for w in verb.rights:
        if (w.dep_ in ('agent')):
            return verb.doc[verb.i:w.i + 1]

    # rule 3: <PERSON/nsubj> <is/VERB> the <president/attr> of
    for w in verb.rights:
        if (w.dep_ in ('attr')):
            return _extend_lefts(w)

    # rule 4: merge verb with dobj if none entity
    dobj = next(filter(lambda w: w.dep_ in ('dobj', 'obj'), verb.rights), None)
    if (None != dobj):
        # 4.1 - dative: '<PERSON/nsubj> <gave/VERB> <testimony/dobj> <to/dative> ...'
        for w in verb.rights:
            if (w.dep_ in ('dative')):
                return verb.doc[verb.i:w.i + 1]
        # 4.2 - prep: '<PERSON/nsubj> <had/VERB> a <debate/dobj> <with/prep> <PERSON/pobj>...'
        for w in dobj.rights:
            if (w.dep_ in ('prep', 'nmod')):
                return verb.doc[dobj.i:dobj.i+1]

    return verb.doc[verb.i:verb.i+1]


def _extract_objects(verb, entities_only=True):
    ''' return objects in (s,v,o) related to given VERB '''

    # rule 1: verb -> dobj
    # (e.g: <PERSON/nsubj> <killed/verb> <PERSON/dobj>)
    for dobj in filter(lambda w: w.dep_ in ('dobj', 'obj'), verb.rights):
        if (entities_only and 0 == dobj.ent_type):
            continue  # skip none-entity
        return _right_conj(dobj)

    # rule 2: verb-span (including: prep/dative/agent) -> pobj
    # (e.g: <PERSON/nsubj> <killed by/verb-span> <PERSON/pobj>)
    for pobj in filter(lambda w: w.dep_ == 'pobj', verb.rights):
        if (entities_only and 0 == pobj.ent_type):
            continue  # skip none-entity
        return _right_conj(_extend_lefts(pobj))

    # rule 3: verb -> prep/dative/agent -> pobj
    # (e.g: <PERSON/nsubj> <met/verb> <with/prep> <PERSON/pobj>)
    for prep in filter(lambda w: w.dep_ in ('prep', 'dative', 'agent'), verb.rights):
        for pobj in filter(lambda w: w.dep_ in ('pobj'), prep.children):
            if (entities_only and 0 == pobj.ent_type):
                continue  # skip none-entity
            return _right_conj(_extend_lefts(pobj))

    for obj in filter(lambda w: w.dep_ in ('nmod'), verb.rights):
        if (entities_only and 0 == obj.ent_type):
            continue  # skip none-entity
        return _right_conj(obj)
    return []  # None


def _extend_lefts(w):
    start = end = w.i
    for left in filter(lambda t: t.pos_ == w.pos_ or t.dep_ in ('compound', 'amod'), w.lefts):
        start = left.i
    return w.doc[start:end + 1]


def _left_conj(span):
    ''' yield span and any left conjunctions'''
    yield span
    for conj in filter(lambda w: w.dep_ == 'conj', span.lefts):
        yield _extend_lefts(conj)


def _right_conj(span):
    ''' yield span and any right conjunctions'''
    yield span
    for conj in filter(lambda w: w.dep_ == 'conj', span.rights):
        yield _extend_lefts(conj)


def is_neg(v):
    for w in v.lefts:
        if (w.dep_ == 'neg'):
            return True
    return False
