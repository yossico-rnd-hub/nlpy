# wsnlp
nlp processor based on spacy

## install virtualenv python3
virtualenv -p python3 nlp

# packages
env/bin/pip install spacy
env/bin/pip install flask
env/bin/pip install jsonpickle

### en
env/bin/python -m spacy download en
env/bin/python -m spacy download en_core_web_sm
env/bin/python -m spacy download en_core_web_md
env/bin/python -m spacy download en_core_web_lg

### es
env/bin/python -m spacy download es
env/bin/python -m spacy download es_core_news_sm
env/bin/python -m spacy download es_core_news_md

## misc
spacy.explain('pobj')

## TODO
- similarity (spacy)
- categorization (spacy: TextCategorizer - https://spacy.io/api/textcategorizer)
- relations (spacy)
- tagger
- env/bin/pip install --upgrade gensim
- training (git): spaCy/examples/training
- displayCy
- https://github.com/conllul/UL_Hebrew-HTB

### relations
- relations extensions 
  - (like spacy tokens: https://spacy.io/usage/linguistic-features#section-tokenization)
  - relations.add_rule(function(doc))
- review en_extract_preposition_relations (should we start from subject?)
- label=PERSON when comes before PERSON-PRED
  e.g: 
  - Hillery killed David.
    ( Hillery/ORG, killed, David/PERSON )
  - Hillery is the step mother of Chelsea.
    ( Hillery/ORG, step mother, Chelsea/ORG )
