#!nlp/bin/python

import sys
import argparse
import os
import os.path
import requests
import logging
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from nlp import Document, Entity
from types import SimpleNamespace as Namespace

def is_hidden(f):
    # linux
    return len(f) > 1 and f[0] == '.' and f[1] != '/'

class Scoring(object):
    def __init__(self, precision = 0, recall = 0, f1score = 0):
        self.precision = precision
        self.recall = recall
        self.f1score = f1score

class Gold(Document):
    def __init__(self, file):
        # try loading the corresponding gold file
        file = os.path.basename(file)
        file = os.path.join(os.path.dirname(__file__), 'gold', file + '.gold')
        self.from_json_file(file)

    def scoring(self, doc):
        '''
        produces a scoring (precision, recall & f1score) for the given doc entities.
        '''
        # lilo:TODO - calculate per class, then overall
        true_positives = 0
        false_positives = 0
        false_negatives = 0

        sorted(doc.entities, key=lambda x: x.start_char)
        sorted(self.entities, key=lambda x: x.start_char)

        doc_index = 0
        gold_index = 0

        doc_entities_len = len(doc.entities)
        gold_entities_len = len(self.entities)

        while True:
            if (doc_index < doc_entities_len):
                e_doc = doc.entities[doc_index]
            else:
                e_doc = None

            if (gold_index < gold_entities_len):
                e_gold = self.entities[gold_index]
            else:
                e_gold = None

            if (None == e_doc and None == e_gold):
                break # done

            if (None != e_doc and None == e_gold):
                # only e_doc valid => false positive
                false_positives += 1
                doc_index += 1
                continue

            if (None == e_doc and None != e_gold):
                # only e_gold valid => false negative
                false_negatives += 1
                gold_index += 1
                continue

            # both valid
            overlapping_score = self.test_overlapping(e_doc, e_gold)
            if (overlapping_score >= 0.5):
                doc_index += 1
                gold_index += 1
                if (e_doc.label == e_gold.label):
                    true_positives += 1 # successful match!
                    continue
                # overlap but labels do not match!
                false_positives += 1
                false_negatives += 1
                continue
            
            # overlapping < 0.5 (no match!)
            if (e_doc.start_char < e_gold.start_char):
                false_positives += 1
                doc_index += 1
                continue
            if (e_gold.start_char < e_doc.start_char):
                false_negatives += 1
                gold_index += 1
                continue

        precision = true_positives / (true_positives + false_positives)
        recall = true_positives / (true_positives + false_negatives) 
        f1score = 2 * (precision * recall) / (precision + recall)
        scoring = Scoring(precision, recall, f1score)
        return scoring
    
    def test_overlapping(self, e_doc, e_gold):
        '''
        test if and how much the doc entity overlaps the gold antity.\n
        return a real value in the range [0.0, 1.0].
        '''
        
        start = max(e_gold.start_char, e_doc.start_char)
        end = min(e_gold.end_char, e_doc.end_char)
        num_overlapping_chars = end - start
        if (num_overlapping_chars <= 0):
            return 0.0
        
        return float(num_overlapping_chars) / (e_gold.end_char - e_gold.start_char)

class GoldTest(object):
    """
    Nlp test class\n
    compute scoring (precision, recall & f1score) for the given file/directory
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='this module is used for nlp testing.')
        self.parser.add_argument('file', type=str, help='file to process')

    def run(self, debug = False):
        '''
        given a file or directory:\n
        compute scoring (precision, recall & f1score).\n
        output for a single file - scoring for that file.\n
        output for a directory - scoring for all files (recursively).
        '''

        self.debug = debug

        # read command-line args
        args = self.parser.parse_args()
        file = args.file

        # process input (file/directory)
        scoring = [] # result scoring

        # assume a directory
        if (not self.process_directory(file, scoring)):
            # for convinience we assume file may reside inside the 'test/docs' folder    
            if (not os.path.isfile(file)):
                # try under test/docs folder
                file = os.path.join(os.path.dirname(__file__), 'docs', file)
                if (not os.path.isfile(file)):
                    print('file not found: ' + file)
                    exit(-1)
            self.process_file(file, scoring)

    def process_directory(self, dir, scoring):
        '''
        recursively process all files and sub-directories in given dir.\n
        return True if dir is a directory, False otherwise
        '''

        # must be a directory
        if (not os.path.isdir(dir)):
            return False

        # skip hidden directories
        dir = dir.strip()
        if (is_hidden(dir)):
            return True

        # process all files & sub-directories recursively
        for f in os.listdir():
            if (os.path.isdir(f)):
                self.process_directory(f, scoring)
            elif (os.path.isfile(f)):
                self.process_file(f, scoring)
            #else: ignore
        
        return True

    def process_file(self, file, scoring):
        '''
        process text file (REST call to nlp-service to extract e.g., entities)
        than, compute the scoring of the labeling using a corresponding gold 
        with the name of the same file under the test/gold directory.\n
        the labled document and its scoring are appended to the supplied scoring list.
        '''

        # skip hidden files
        file = file.strip()
        if (is_hidden(file)):
            return 0

        # read text file
        text = ''
        try:
            with open(file, 'r') as myfile:
                text = myfile.read()
        except Exception as e:
            logging.exception(e)
            logging.error('failed to read file: ' + file)
            return False
        else:
            # process file (nlp-service)
            try:
                url = 'http://localhost:5000/api/v1.0/docs'
                data = { 'text': text }
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                json_doc = requests.post(url, data=json.dumps(data), headers = headers)

                doc = Document()
                doc.text = text
                doc.entities = doc.entities_from_json(json_doc.text)
            except Exception as e:
                logging.exception(e)
                logging.error('http failed!\n' + url)
                return False
            else:
                gold = Gold(file)
                s = gold.scoring(doc)
                scoring.append((doc, s))

                #lilo
                if (True == self.debug):
                    print(json_doc.text)
                    print('')
                    print('precision: {}'.format(s.precision))
                    print('recall: {}'.format(s.recall))
                    print('f1score: {}'.format(s.f1score))

                return True

gold_test = GoldTest()

if __name__ == '__main__':
    gold_test.run(debug=True)
