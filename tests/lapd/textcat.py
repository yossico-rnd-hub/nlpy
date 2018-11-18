#!env/bin/python

from __future__ import unicode_literals, print_function
import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, decaying, compounding

import csv
import random
from math import log

use_titles = True

def read_data(path):
    texts = []
    labels = []
    with path.open('r') as file_:
        for row in csv.DictReader(file_, delimiter=','):
            text = row['title'] if use_titles else row['text']
            text_labels = row['labels']  # there may be multiple labels per row
            for label in text_labels.split(','):
                texts.append(text)
                labels.append(label.strip())
    return texts, labels


def format_data_for_spacy(texts, labels, all_labels):
    ys = []
    for true_label in labels:
        cats = {wrong_label: 0.0 for wrong_label in all_labels}
        cats[true_label] = 1.
        ys.append({'cats': cats})
    return list(zip(texts, ys))


@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_texts=("Number of texts to train from", "option", "t", int),
    n_iter=("Number of training iterations", "option", "n", int))
def main(model=None, output_dir=None, n_iter=20, n_texts=2000):
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')  # create blank Language class
        print("Created blank 'en' model")

    # add the text classifier to the pipeline if it doesn't exist
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'textcat' not in nlp.pipe_names:
        textcat = nlp.create_pipe('textcat')
        nlp.add_pipe(textcat, last=True)
    # otherwise, get it, so we can add labels to it
    else:
        textcat = nlp.get_pipe('textcat')


if __name__ == '__main__':
    plac.call(main)
