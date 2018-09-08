#!nlp/bin/python

import argparse
import os
import os.path
import requests
import logging
import json

class NlpTest(object):
    """Nlp test class"""
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='this module is used for nlp testing.')
        self.parser.add_argument('file', type=str, help='file to process')

    def run(self, debug = False):
        # lilo
        # args = self.parser.parse_args()
        # file = args.file
        file = 'text1'
        if not os.path.isfile(file):
            # try under test/docs folder
            file = os.path.join(os.path.dirname(__file__), 'docs', file)
            if not os.path.isfile(file):
                print('file not found: ' + file)
                exit(-1)

        # read text file
        text = ''
        try:
            with open(file, 'r') as myfile:
                text = myfile.read()
        except:
            logging.error('filed to read file: ' + file)

        try:
            url = 'http://localhost:5000/api/v1.0/docs'
            data = { 'text': text }
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            res = requests.post(url, data=json.dumps(data), headers = headers)
            print(res.text)
        except:
            logging.error('http failed!\n' + url + '\n' + data)

app = NlpTest()

if __name__ == '__main__':
    app.run(debug=True)
