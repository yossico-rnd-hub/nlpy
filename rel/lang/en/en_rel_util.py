def extract_when(pred):
    date_list = [w for w in pred.subtree if w.ent_type_ == 'DATE']
    when = date_list[0] if date_list else None
    if (None != when and when.dep_ == 'compound'):
        when = when.doc[min(when.i, when.head.i): max(when.i, when.head.i)+1]
    return when
