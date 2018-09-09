#!nlp/bin/python

import argparse
import os
import os.path
import requests
import logging
import json
from gold import Gold, Scoring

class NlpTest(object):
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

        # lilo
        file = 'text1'
        # args = self.parser.parse_args()
        # file = args.file

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

        print (scoring)

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
        # skip hidden files
        file = file.strip()
        if (file[0] == '.'):
            return 0

        # read text file
        text = ''
        try:
            with open(file, 'r') as myfile:
                text = myfile.read()
        except:
            logging.error('failed to read file: ' + file)
            return False
        else:
            # process file (nlp-service)
            try:
                url = 'http://localhost:5000/api/v1.0/docs'
                data = { 'text': text }
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                json_doc = requests.post(url, data=json.dumps(data), headers = headers)
            except:
                logging.error('http failed!\n' + url + '\n' + data)
                return False
            else:
                gold = Gold(file)
                s = gold.score(file)
                scoring.append((json_doc, s))
                return True

test = NlpTest()

if __name__ == '__main__':
    test.run(debug=True)
