CORPUS_EN = [
    {'text': u'When Sebastian Thrun started working on self-driving cars at '
     u'Google in 2007, few people outside of the company took him '
     u'seriously. “I can tell you very senior CEOs of major American '
     u'car companies would shake my hand and turn away because I wasn’t '
     u'worth talking to,” said Thrun, now the co-founder and CEO of '
     u'online higher education startup Udacity, in an interview with '
     u'Recode earlier this week.',
        'relations': [('Sebastian Thrun', 'started working', 'Google', '2007'),
                      ('Thrun', 'CEO of', 'Udacity', 'now')]},

    {'text': 'Hillary Clinton met secretly with Barak Obama last week.',
        'relations': [('Hillary Clinton', 'met', 'Barak Obama', 'last week')]},
    {'text': 'Donald Trump debate with Barak Obama and Hillary Clinton last Tuesday.',
        'relations': [('Donald Trump', 'debate', 'Barak Obama', 'last Tuesday'),
                      ('Donald Trump', 'debate', 'Hillary Clinton', 'last Tuesday')]},

    {'text': 'Last week Hillary, mother of Chelsea and Dan, met with congressman Mike Pence in the White House.',
        'relations': [('Hillary', 'met', 'Mike Pence', 'Last week'),
                      ('Hillary', 'mother of', 'Chelsea', None),
                      ('Hillary', 'mother of', 'Dan', None)]},
    {'text': 'Mark Zuckerberg, CEO of Facebook, gave testimony to the U.S. Senate Sunday morning.',
        'relations': [('Mark Zuckerberg', 'gave testimony', 'the U.S. Senate', 'Sunday morning'),
                      ('Mark Zuckerberg', 'CEO of', 'Facebook', None)]},

    {'text': 'Hillery killed David.',
        'relations': [('Hillery', 'killed', 'David', None)]},

    {'text': 'David killed by Hillery.',
        'relations': [('David', 'killed by', 'Hillery', None)]},

    # is_a / is_the / is_not / did_not
    {'text': 'Bill is the president of the U.S.',
        'relations': [('Bill', 'president', 'U.S.', None)]},
    {'text': 'George Washington was the first president of the U.S.',
        'relations': [('George Washington', 'first president', 'U.S.', None)]},
    {'text': 'Hillery is the biologic mother of Chelsea.',
        'relations': [('Hillery', 'biologic mother', 'Chelsea', None)]},
    {'text': 'Hillery is the step mother of Chelsea.',
        'relations': [('Hillery', 'step mother', 'Chelsea', None)]},
    {'text': 'Hillery is not the mother of Bill.',
        'relations': []},
    {'text': 'Hillery did not meet with Bill.',
        'relations': []},
]
