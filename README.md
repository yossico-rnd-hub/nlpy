# wsnlp
nlp processor based on spacy

## install virtualenv python3
virtualenv -p python3 env

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

### training (es)
git clone https://github.com/UniversalDependencies/UD_Spanish-AnCora
mkdir ancora-json
python -m spacy convert UD_Spanish-AnCora/es_ancora-ud-train.conllu ancora-json
python -m spacy convert UD_Spanish-AnCora/es_ancora-ud-dev.conllu ancora-json
mkdir models
python -m spacy train es models ancora-json/es_ancora-ud-train.json ancora-json/es_ancora-ud-dev.json

python -m spacy package -f {best_model} dist/
cd dist/{model_name}
python setup.py sdist

### jupiter notebook virtual env
env/bin/pip install ipykernel
env/bin/ipython kernel install --user --name=env

### textacy
env/bin/pip install textacy
env/bin/pip install textacy[lang] (for language detection)

## TODO
- similarity (spacy)
- categorization (spacy: TextCategorizer - https://spacy.io/api/textcategorizer)
- tagger
- env/bin/pip install --upgrade gensim
- training (git): spaCy/examples/training
- displayCy
- https://github.com/conllul/UL_Hebrew-HTB

### entities
- label=PERSON when comes before PERSON-PRED
  e.g: 
  - Hillary killed David.
    ( Hillary/ORG, killed, David/PERSON )
  - Hillary is the step mother of Chelsea.
    ( Hillary/ORG, step mother, Chelsea/ORG )

### relations
- multiple predicates: '... co-founder and CEO of Udacity' (noun_chunks?)
- textacy
- spanish
- basis
