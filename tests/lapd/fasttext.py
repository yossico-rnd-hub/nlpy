#!env/bin/python

import csv
import plac
import random
from pathlib import Path

use_titles = False


@plac.annotations(
    data_dir=("data directory", "option", "i", Path),
    n_iter=("Number of training iterations", "option", "n", int))
def main(data_dir='data/lapd.labeled', n_iter=20):
    generate_fasttext_train_test_files(data_dir)


def generate_fasttext_train_test_files(data_dir):
    texts, labels = load_data(data_dir)
    data = format_data_for_fasttext(texts, labels)

    split = 0.8
    random.shuffle(data)
    split = int(len(data) * split)
    train_data = data[:split]
    test_data = data[split:]
    print("Using {} examples ({} training, {} evaluation)"
          .format(len(texts), len(train_data), len(test_data)))

    # write train
    ft_train = 'out/crime.train'
    print('writing {} ...'.format(ft_train))
    with open(ft_train, 'w') as _file:
        for item in train_data:
            _file.write("{}\n".format(item))

    # write test
    ft_test = 'out/crime.test'
    print('writing {} ...'.format(ft_test))
    with open(ft_test, 'w') as _file:
        for item in test_data:
            _file.write("{}\n".format(item))

    print('Done.')


def load_data(data_dir):
    print()
    print("loading data from '{}'...".format(data_dir))
    data_dir = Path(data_dir)
    texts = []
    labels = []
    # for year in ['2018']:
        # for year in ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']:
    for year in ['1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']:
        csv_path = data_dir / 'lapd_news_{}.csv'.format(year)
        if csv_path.exists():
            t, l = load_data_file(csv_path)
            labels = labels + l  # array concatination
            texts = texts + t   # array concatination
    return texts, labels


def load_data_file(path):
    texts = []
    labels = []
    with path.open('r') as file_:
        for row in csv.DictReader(file_, delimiter=','):
            # text
            text = row['title'] if use_titles else row['text']
            texts.append(text)
            # labels (there may be multiple labels per row, sparated by '|')
            raw_labels = row['labels']
            labels_list = list(
                map(lambda label: label.strip(), raw_labels.split('|')))
            labels.append(labels_list)
    return texts, labels


def format_data_for_fasttext(texts, labels):
    labeled_texts = []
    for i, labels_list in enumerate(labels):
        ft_labels = ' '.join('__label__{}'.format(label)
                             for label in labels_list)
        labeled_texts.append('{} {}'.format(ft_labels, texts[i]))
    return labeled_texts


if __name__ == '__main__':
    plac.call(main)
