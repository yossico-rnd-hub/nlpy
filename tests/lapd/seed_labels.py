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

# lilo
MAX_FILES = -1
MAX_TITLES = -1

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
    ('DEATH', 'dead'),
    ('DRUGS', 'drugs'),
    ('EMBEZZLEMENT', 'embezzlement'),
    ('EXTORTION', 'extortion'),
    ('FRAUD', 'fraud'),
    ('GAMBLING', 'gambling'),
    ('HARASSMENT', 'harassment'),
    ('HIT_AND_RUN', 'hit and run'),
    ('HIT_AND_RUN', 'hit & run'),
    ('HOME_INVASION', 'home invasion'),
    ('INJURY', 'injur'),
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
    ('CAR_THEFT', 'Car Thieves'),
    ('TORTURE', 'torture'),
    ('TRAFFIC_VIOLATIONS', 'traffic violations'),
    ('TRAFFIC_VIOLATIONS', 'Drunk Driver'),
]


@plac.annotations(
    dir_in=("input directory to read from", "option", "i", str),
    dir_out=("output directory", "option", "o", str),
)
def main(dir_in='data/lapd', dir_out='data/lapd.labeled'):
    if not os.path.exists(dir_in):
        print("no such directory: '{}'".format(dir_in))
        return

    if not os.path.exists(dir_out):
        os.makedirs(dir_out)

    for label, phrase in CRIME_PHRASES:
        doc = nlp(phrase)
        pattern = []
        for w in doc:
            pattern.append({'lemma': '{}'.format(w.lemma_)})
        matcher.add(label, None, pattern)

    tagged = []
    untagged = []
    for filename in os.listdir(dir_in)[:MAX_FILES]:
        filename_in = os.path.join(dir_in, filename)
        filename_out = os.path.join(dir_out, filename)
        print(filename_in)
        with open(filename_in, 'r') as csv_in, open(filename_out, 'w') as csv_out:
            reader = csv.reader(csv_in)
            writer = csv.writer(csv_out)
            header = csv_in.readline()
            header_out = 'labels,' + header
            csv_out.write(header_out)

            next(reader, None)

            i = 0
            for row in reader:
                i += 1
                if MAX_TITLES > 0 and i > MAX_TITLES:
                    break
                title = row[0]
                labels = get_labels(title)
                if (len(labels) > 0):
                    tagged.append((labels, title))
                else:
                    untagged.append(title)
                labels_out = ';'.join(labels) if len(labels) > 0 else 'NONE'
                row.insert(0, labels_out)
                writer.writerow(row)

    # lilo
    # for t in tagged[:10]:
    #     print(t)
    # for t in untagged[:5]:
    #     print(t)


def write_annotated():
    # lilo:TODO
    with open("infile.csv") as f_in, open("outfile.csv", 'w') as f_out:
        # Write header unchanged
        header = f_in.readline()
        f_out.write(header)

        # Transform the rest of the lines
        for line in f_in:
            f_out.write(line.lower())


def get_labels(text):
    #doc = nlp(normalize(text))
    doc = nlp(text)
    matches = matcher(doc)

    labels = []
    for match_id, _, _ in matches:
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
