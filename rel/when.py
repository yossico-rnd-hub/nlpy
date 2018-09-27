import spacy


def extract_when(pred_span):
    pred_head = pred_span[0].head
    when = next(filter(lambda w: w.ent_type_ in (
        'DATE', 'TIME'), pred_head.subtree), None)
    if (None != when):
        if (when.dep_ in ('amod', 'compound')):
            return when.doc[when.i: when.head.i+1]  # extend right
        return when.doc[when.i:when.i+1]
    return None
