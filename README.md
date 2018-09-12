# wsnlp
nlp processor based on spacy

## install virtualenv python3
virtualenv -p python3 nlp

# packages
nlp/bin/pip install spacy
nlp/bin/pip install flask
nlp/bin/pip install jsonpickle

### en
nlp/bin/python -m spacy download en_core_web_sm
nlp/bin/python -m spacy download en_core_web_md
nlp/bin/python -m spacy download en_core_web_lg

### es
nlp/bin/python -m spacy download es
nlp/bin/python -m spacy download es_core_news_sm
nlp/bin/python -m spacy download es_core_news_md

## TODO
- similarity (spacy)
- categorization (spacy: TextCategorizer - https://spacy.io/api/textcategorizer)
- relations (spacy)
- tagger
- nlp/bin/pip install --upgrade gensim
- training (git): spaCy/examples/training
- displayCy