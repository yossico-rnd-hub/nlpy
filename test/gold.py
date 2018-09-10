#!nlp/bin/python

import sys
import argparse
import os
import os.path
import requests
import logging
import json
import jsonpickle

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from nlp import Document, Entity
from types import SimpleNamespace as Namespace

class Scoring(object):
    def __init__(self, precision = 0, recall = 0, fscore = 0):
        self.precision = precision
        self.recall = recall
        self.fscore = fscore

class Gold(Document):
    def __init__(self, file):
        # try loading the corresponding gold file
        file = os.path.basename(file)
        file = os.path.join(os.path.dirname(__file__), 'gold', file + '.gold')
        with open(file, 'r') as f:
            self.file = file
            self.gold = jsonpickle.decode(f.read())
        
        #lilo:TODO

    def test_match(self, e):
        '''
        test if and how much the given entity matches a gold antity.\n
        return a real value in [0,1]
        '''
        #lilo: TODO
        return 0.0

    def scoring(self, doc):
        '''
        produces a scoring (precision, recall & fscore) for the given doc entities.
        '''
        # lilo:TODO
        # calculate per class, then overall
        true_positives = 0
        false_positives = 0
        true_negatives = 0
        false_negatives = 0

        # for (e in doc.entities):
        #     match = test_match(e)

        scoring = Scoring()
        return scoring

class GoldTest(object):
    """
    Nlp test class\n
    compute scoring (precision, recall & fscore) for the given file/directory
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='this module is used for nlp testing.')
        self.parser.add_argument('file', type=str, help='file to process')

    def run(self, debug = False):
        '''
        given a file or directory:\n
        compute scoring (precision, recall & fscore).\n
        output for a single file - scoring for that file.\n
        output for a directory - scoring for all files (recursively).
        '''

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
        if (dir[0] == '.'):
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
        if (file[0] == '.'):
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
                doc.entities = jsonpickle.decode(json_doc.text)
            except Exception as e:
                logging.exception(e)
                logging.error('http failed!\n' + url)
                return False
            else:
                gold = Gold(file)
                s = gold.scoring(doc)
                scoring.append((doc, s))
                return True

gold_test = GoldTest()

if __name__ == '__main__':
    gold_test.run(debug=True)
