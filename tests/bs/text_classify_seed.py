#!env/bin/python

import os
import csv
import plac

import gensim
from gensim.parsing.preprocessing import preprocess_string

import spacy
from spacy.matcher import Matcher

nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)

CRIME_PHRASES = [
    ('ADULTERY', 'adultery'),
    ('ARSON', 'arson'),
    ('ASSASSINATION', 'assassination'),
    ('ASSAULT', 'assault'),
    ('BLACKMAIL', 'blackmail'),
    ('BRIBERY', 'bribery'),
    ('BURGLARY', 'burglary'),
    ('CAR_THEFT', 'car theft'),
    ('CHILD_ABUSE', 'child abuse'),
    ('DETH', 'dead'),
    ('DRUGS', 'drugs'),
    ('EMBEZZLEMENT', 'embezzlement'),
    ('EXTORTION', 'extortion'),
    ('FRAUD', 'fraud'),
    ('GAMBLING', 'gambling'),
    ('HARASSMENT', 'harassment'),
    ('HIT_AND_RUN', 'hit and run'),
    ('HOME_INVASION', 'home invasion'),
    ('INJURY', 'injure'),
    ('INJURY', 'injury'),
    ('INTIMIDATION', 'intimidation'),
    ('INVASION_OF_PRIVACY', 'invasion of privacy'),
    ('KIDNAPPING', 'kidnapping'),
    ('KIDNAPPING', 'kidnup'),
    ('KILLING', 'killing'),
    ('MANSLAUGHTER', 'manslaughter'),
    ('MISSING', 'missing'),
    ('MURDER', 'murder'),
    ('MURDER', 'manslaughter'),
    ('MURDER', 'homicide'),
    ('MURDER', 'homoside'),
    ('PERJURY', 'perjury'),
    ('RAPE', 'rape'),
    ('ROBBERY', 'robber'),
    ('ROBBERY', 'robbery'),
    ('SEXUAL_ASSAULT', 'sexual assault'),
    ('SEXUAL_ASSAULT', 'sexual offences'),
    ('SHOOTING', 'shooting'),
    ('SHOOTING', 'shot'),
    ('SMUGGLING', 'smuggling'),
    ('SODOMY', 'sodomy'),
    ('STABBING', 'stabbing'),
    ('STRUCK', 'struck'),
    ('SUICIDE', 'suicid'),
    ('SUICIDE', 'suicide'),
    ('THEFT', 'theft'),
    ('THEFT', 'stolen property'),
    ('THEFT', 'thiev'),
    ('TORTURE', 'torture'),
    ('TRAFFIC_VIOLATIONS', 'traffic violations'),
    ('TRAFFIC_VIOLATIONS', 'Drunk Driver'),
]


@plac.annotations(
    dir=("input directory to read from", "option", "d", str))
def main(dir='out'):
    if not os.path.exists(dir):
        print("no such directory: '{}'".format(dir))
        return

    for label, phrase in CRIME_PHRASES:
        doc = nlp(phrase)
        pattern = []
        for w in doc:
            pattern.append({'lemma': '{}'.format(w.lemma_)})
        matcher.add(label, None, pattern)

    tagged = []
    untagged = []
    for filename in os.listdir(dir)[:1]:
        filename = os.path.join(dir, filename)
        print(filename)
        with open(filename, 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)
            i = 0
            for row in reader:
                i += 1
                if i > 10:
                    break
                title = row[0]
                labels = get_labels(title)
                if (len(labels) > 0):
                    tagged.append((labels, title))
                else:
                    untagged.append(title)

    for t in tagged[:5]:
        print(t)
    for t in untagged[:5]:
        print(t)


def get_labels(text):
    doc = nlp(normalize(text))
    matches = matcher(doc)

    labels = []
    for match_id, start, end in matches:
        label = nlp.vocab.strings[match_id]
        labels.append(label)

    if (len(labels) > 0):
        distinct = set(labels)
        return distinct

    return labels


def normalize(text):
    normalized = gensim.parsing.preprocessing.preprocess_string(text)
    return ' '.join(normalized)


if __name__ == '__main__':
    plac.call(main)
