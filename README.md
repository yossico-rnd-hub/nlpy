# nlpy

nlp playground based on spacy

## test service

process full nlp pipeline
Usage:
curl -i -H "Content-Type: application/json" -X POST -d '{"text": "foo", "model": "en"}' http://localhost:5000/nlp

## install virtualenv python3

virtualenv -p python3 env

## packages

env/bin/pip install spacy
env/bin/pip install flask
env/bin/pip install jsonpickle

### spacy version

env/bin/python -c "import os; import spacy; print(spacy.__version__)"

### en

env/bin/python -m spacy download en
env/bin/python -m spacy download en_core_web_sm
env/bin/python -m spacy download en_core_web_md
env/bin/python -m spacy download en_core_web_lg

### es

env/bin/python -m spacy download es
env/bin/python -m spacy download es_core_news_sm
env/bin/python -m spacy download es_core_news_md

### jupiter notebook virtual env

env/bin/pip install ipykernel
env/bin/ipython kernel install --user --name=env

## training (es)

git clone https://github.com/UniversalDependencies/UD_Spanish-AnCora
mkdir ancora-json
python -m spacy convert UD_Spanish-AnCora/es_ancora-ud-train.conllu ancora-json
python -m spacy convert UD_Spanish-AnCora/es_ancora-ud-dev.conllu ancora-json
mkdir models
python -m spacy train es models ancora-json/es_ancora-ud-train.json ancora-json/es_ancora-ud-dev.json

python -m spacy package -f {best_model} dist/
cd dist/{model_name}
python setup.py sdist

## TODO

- understand spacy code
- KGs
- Training a parser for custom semantics (test/spacy/train_intent_parser.py, see: relations below)
  - https://spacy.io/usage/training#intent-parser
- Training a text classification model (test/spacy/train_textcat.py)
  - https://spacy.io/usage/training#textcat
- doc similarity (spacy)
- categorization (spacy: TextCategorizer - https://spacy.io/api/textcategorizer)

### textacy

env/bin/pip install textacy
env/bin/pip install textacy[lang] (for language detection)

### misc

- displayCy
- tagger (prodigy)
- basis (compare performance)
- training (git): spaCy/examples/training
- env/bin/pip install --upgrade gensim
- https://github.com/conllul/UL_Hebrew-HTB
- other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
  with nlp.disable_pipes(*other_pipes):  # only train NER

### entities

- label=PERSON when comes before PERSON-PRED
  e.g:
  - Hillary killed David.
    ( Hillary/ORG, killed, David/PERSON )
  - Hillary is the step mother of Chelsea.
    ( Hillary/ORG, step mother, Chelsea/ORG )

### relations

- Training a parser for custom semantics:
  - https://spacy.io/usage/training#intent-parser
  - test/spacy/train_intent_parser.py
- multiple predicates: '... co-founder and CEO of Udacity' (noun_chunks?)
