#!env/bin/python

import argparse
import requests
import json


class TestNLP(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='test nlp-service entity extraction.')
        self.parser.add_argument(
            '-f', '--file', help='path of file to process')
        self.parser.add_argument(
            '-t', '--text', help='text to process (within single quotes)')
        self.parser.add_argument('-m', '--model', help='model to use (e.g: en/es)')

    def run(self):
        args = self.parser.parse_args()

        if args.text:
            text = args.text
        elif args.file:
            with open(args.file, 'r') as f:
                text = f.read()
        else:
            text = (u"When Sebastian Thrun started working on self-driving cars at "
                    u"Google in 2007, few people outside of the company took him "
                    u"seriously. “I can tell you very senior CEOs of major American "
                    u"car companies would shake my hand and turn away because I wasn’t "
                    u"worth talking to,” said Thrun, now the co-founder and CEO of "
                    u"online higher education startup Udacity, in an interview with "
                    u"Recode earlier this week.")

        default_model = 'en_core_web_sm'  # default model
        model = args.model if args.model else default_model

        data = {'text': text, 'model': model}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        url = 'http://localhost:5000/nlp'
        json_doc = requests.post(url, data=json.dumps(data), headers=headers)

        if not args.text:
            print()
            print(text)
            print()
        print(json_doc.text)


if __name__ == '__main__':
    test = TestNLP()
    test.run()
