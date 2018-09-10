#!nlp/bin/python

import requests
import json

def test():
    text = (u"When Sebastian Thrun started working on self-driving cars at "
        u"Google in 2007, few people outside of the company took him "
        u"seriously. “I can tell you very senior CEOs of major American "
        u"car companies would shake my hand and turn away because I wasn’t "
        u"worth talking to,” said Thrun, now the co-founder and CEO of "
        u"online higher education startup Udacity, in an interview with "
        u"Recode earlier this week.")

    data = { 'text': text }
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    url = 'http://localhost:5000/api/v1.0/docs'
    json_doc = requests.post(url, data=json.dumps(data), headers = headers)
    print(json_doc.text)

if __name__ == '__main__':
    test()
