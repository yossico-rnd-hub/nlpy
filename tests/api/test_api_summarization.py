#!env/bin/python

import argparse
import requests
import json


class Test(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='test wordmap.')
        self.parser.add_argument(
            '-f', '--file', help='path of file to process')
        self.parser.add_argument(
            '-t', '--text', help='text to process (within single quotes)')

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
                    u"Recode earlier this week. "
                    u"We do NOT want to merge entities like Hillary Clinton and Bill Clinton  ."
                    )

        data = {'text': text, 'word_count': 100}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        url = 'http://localhost:5000/nlp/summarization'
        res = requests.post(url, data=json.dumps(data), headers=headers)
        print(res.text)


if __name__ == '__main__':
    test = Test()
    test.run()
