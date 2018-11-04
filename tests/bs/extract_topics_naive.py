#!env/bin/python

import os
import csv
import plac

import gensim
from gensim.parsing.preprocessing import preprocess_string


@plac.annotations(
    dir=("input directory to read from", "option", "d", str))
def main(dir='out'):
    extract_topics(dir=dir)


def extract_topics(dir='out'):
    if not os.path.exists(dir):
        print("no such directory: '{}'".format(dir))
        return

    tagged = []
    untagged = []
    for filename in os.listdir(dir):
        filename = os.path.join(dir, filename)
        # print(filename)
        with open(filename, 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)
            for row in reader:
                title = row[0]
                tags = get_tags(title)
                if (len(tags) > 0):
                    tagged.append((set(tags), title))
                else:
                    untagged.append(title)

    for t in tagged:
        print(t)


CRIME_LIST = [
    'adulteri',
    'arson',
    'assassin',
    'assault',
    'bigami',
    'blackmail',
    'briberi',
    'burglari',
    'car thift',
    'child abuse',
    'dead',
    'drug',
    'embezzl',
    'extort',
    'fraud',
    'gambl',
    'harass',
    'hit',
    'home',
    'homicid',
    'homosid',
    'injur',
    'intimid',
    'kidnap',
    'kidnup',
    'kill',
    'manslaught',
    'miss',  # missing
    'murder',
    'offenc',
    'perjuri',
    'privaci',
    'properti',
    'rape',
    'robber',
    'robberi',
    'run',
    'sexual',
    'shoot',
    'shot',
    'smuggl',
    'sodomi',
    'stab',
    'stolen',
    'struck',
    'suicid',
    'theft',
    'thiev',
    'thift',
    'tortur',
    'traffic',
]


def get_tags(text):
    normalized = normalize(text)
    tags = []
    for w in normalized:
        if w in CRIME_LIST:
            tags.append(w)
    if (len(tags) > 0):
        distinct = set(tags)
        return distinct
    return tags


def normalize(text):
    normalized = gensim.parsing.preprocessing.preprocess_string(text)
    return normalized


CRIME_LIST2 = [
    'adultery bigamy',
    'arson',
    'assassination',
    'assault',
    'blackmail',
    'bribery',
    'burglary',
    'car theft',
    'child abuse',
    'dead',
    'drugs',
    'embezzlement',
    'extortion',
    'fraud',
    'gambling',
    'harassment',
    'hit and run',
    'home invasion',
    'homicide',
    'homoside',
    'injure',
    'injury',
    'intimidation',
    'invasion of privacy',
    'kidnapping',
    'kidnup',
    'killing',
    'manslaughter',
    'missing',
    'murder',
    'perjury',
    'rape',
    'robber',
    'robbery',
    'sexual assault',
    'sexual offences',
    'shooting',
    'shot',
    'smuggling',
    'sodomy',
    'stabbing',
    'stolen property',
    'struck',
    'suicid',
    'suicide',
    'theft',
    'thiev',
    'torture',
    'traffic violations'
]

if __name__ == '__main__':
    plac.call(main)
