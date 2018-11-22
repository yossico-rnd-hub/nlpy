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

CRIME_LIST = [
    ('ABDUCTION', 'abduction'),
    ('ADULTERY', 'adultery'),
    ('ARSON', 'arson'),
    ('ASSASSINATION', 'assassination'),
    ('ASSAULT', 'assault'),
    ('BIGAMY', 'bigamy'),
    ('BLACKMAIL', 'blackmail'),
    ('BOMBING', 'bombing'),
    ('BRIBERY', 'bribery'),
    ('BURGLARY', 'burglary'),
    ('CAR_THEFT', 'Car Thieves'),
    ('CAR_THEFT', 'car theft'),
    ('CHILD_ABUSE', 'child abuse'),
    ('CORRUPTION', 'corruption'),
    ('CYBERCRIME', 'cybercrime'),
    ('DEATH', 'dead'),
    ('DOMESTIC_VIOLENCE', 'domestic violence'),
    ('DRUGS', 'drugs'),
    ('DRUGS', 'narcotic'),
    ('DRUNK_DRIVING', 'drunk driving'),
    ('DRUNKENNESS', 'drunk'),
    ('EMBEZZLEMENT', 'embezzlement'),
    ('ESPIONAGE', 'espionage'),
    ('EXTORTION', 'extortion'),
    ('FORGERY', 'forgery'),
    ('FRAUD', 'fraud'),
    ('GAMBLING', 'gambling'),
    ('GENOCIDE', 'genocide'),
    ('HARASSMENT', 'harassment'),
    ('HIJACKING', 'hijacking'),
    ('HIT_AND_RUN', 'hit & run'),
    ('HIT_AND_RUN', 'hit and run'),
    ('HOME_INVASION', 'home invasion'),
    ('HOMICIDE', 'homicide'),
    ('HOOLIGANISM', 'hooliganism'),
    ('IDENTITY_THEFT', 'identity theft'),
    ('INJURY', 'injur'),
    ('INJURY', 'injure'),
    ('INJURY', 'injury'),
    ('INTIMIDATION', 'intimidation'),
    ('INVASION_OF_PRIVACY', 'invasion of privacy'),
    ('KIDNAPPING', 'kidnapping'),
    ('KIDNAPPING', 'kidnup'),
    ('KILLING', 'killing'),
    ('LIBEL', 'libel'),
    ('LOITERING', 'loitering'),
    ('LOOTING', 'looting'),
    ('LYNCHING', 'lynching'),
    ('MANSLAUGHTER', 'manslaughter'),
    ('MASSACRE', 'massacre'),
    ('MISSING', 'missing'),
    ('MUGGING', 'mugging'),
    ('MURDER', 'homicide'),
    ('MURDER', 'homoside'),
    ('MURDER', 'manslaughter'),
    ('MURDER', 'murder'),
    ('PERJURY', 'perjury'),
    ('PICKPOCKETING', 'pickpocketing'),
    ('PILFERING', 'pilfering'),
    ('POACHING', 'poaching'),
    ('PORNOGRAPHY', 'pornograpy'),
    ('PROSTITUTION', 'prostitution'),
    ('RAPE', 'rape'),
    ('RIOT', 'riot'),
    ('ROBBERY', 'robber'),
    ('ROBBERY', 'robbery'),
    ('SEXUAL_ASSAULT', 'sexual assault'),
    ('SEXUAL_ASSAULT', 'sexual offences'),
    ('SHOOTING', 'fired at'),
    ('SHOOTING', 'shooting'),
    ('SHOOTING', 'shot'),
    ('SHOPLIFTING', 'shoplifting'),
    ('SLANDER', 'slander'),
    ('SMUGGLING', 'smuggling'),
    ('SODOMY', 'sodomy'),
    ('SPEEDING', 'speeding'),
    ('STABBING', 'stabbing'),
    ('STRUCK', 'struck'),
    ('SUICIDE', 'suicid'),
    ('SUICIDE', 'suicide'),
    ('TERRORISM', 'terrorism'),
    ('THEFT', 'larceny'),
    ('THEFT', 'stolen property'),
    ('THEFT', 'theft'),
    ('THEFT', 'thiev'),
    ('TORTURE', 'torture'),
    ('TRAFFICKING', 'trafficking'),
    ('TRAFFIC_VIOLATIONS', 'Drunk Driver'),
    ('TRAFFIC_VIOLATIONS', 'traffic violations'),
    ('TREASON', 'treason'),
    ('TRESPASS', 'trespass'),
    ('TRESPASSING', 'trespassing'),
    ('VANDALISM', 'vandalism'),
]


@plac.annotations(
    dir_in=("input directory to read from", "option", "i", str),
    dir_out=("output directory", "option", "o", str),
    xxx=("mask text", "flag", "x"),
)
def main(dir_in='data/lapd', dir_out='data/lapd.labeled', xxx=False):
    if not os.path.exists(dir_in):
        print("no such directory: '{}'".format(dir_in))
        return

    if not os.path.exists(dir_out):
        os.makedirs(dir_out)

    with nlp.disable_pipes('ner', 'parser'):
        for label, phrase in CRIME_LIST:
            doc = nlp(phrase)
            pattern = []
            for w in doc:
                pattern.append({'lemma': '{}'.format(w.lemma_)})
            matcher.add(label, None, pattern)

        print("writing labeled output to: '{}'".format(dir_out))
        tagged = []
        untagged = []
        for filename in os.listdir(dir_in)[:MAX_FILES]:
            filename_in = os.path.join(dir_in, filename)
            filename_out = os.path.join(dir_out, filename)
            print(filename_in)
            with open(filename_in, 'r') as csv_in, open(filename_out, 'w') as csv_out:
                reader = csv.reader(csv_in)
                writer = csv.writer(csv_out, delimiter=',')
                header = csv_in.readline()
                header_out = 'labels,' + header
                csv_out.write(header_out)

                next(reader, None)

                i = 0
                for row in reader:
                    i += 1
                    if MAX_TITLES > 0 and i > MAX_TITLES:
                        break
                    title = row[1]
                    labels = get_labels(title)
                    if (len(labels) > 0):
                        tagged.append((labels, title))
                    else:
                        untagged.append(title)
                    labels_out = '|'.join(labels) if len(
                        labels) > 0 else 'NONE'
                    row.insert(0, labels_out)
                    if xxx:
                        text = row[8]
                        row[8] = mask(nlp, matcher, text)
                    writer.writerow(row)

    # lilo
    # for t in tagged[:10]:
    #     print(t)
    # for t in untagged[:5]:
    #     print(t)


def mask(nlp, matcher, text):
    # lilo:TODO
    doc = nlp(normalize(text))
    matches = matcher(doc)

    mask_indices = []
    for _, from_, to_ in matches:
        for i in range(from_, to_):
            mask_indices.append(i)
    mask_indices = set(mask_indices)

    if len(mask_indices) > 0:
        masked_text = ' '.join(t.orth_ if t.i not in mask_indices else 'XXXXX' for t in doc)
        return masked_text
    return text


def write_annotated():
    with open("infile.csv") as f_in, open("outfile.csv", 'w') as f_out:
        # Write header unchanged
        header = f_in.readline()
        f_out.write(header)

        # Transform the rest of the lines
        for line in f_in:
            f_out.write(line.lower())


def get_labels(text):
    doc = nlp(normalize(text))
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
    # return text.lower()
    doc = nlp(text)
    return ' '.join(t.lemma_ for t in doc)
    # normalized = gensim.parsing.preprocessing.preprocess_string(text)
    # return ' '.join(normalized)


if __name__ == '__main__':
    plac.call(main)
