CORPUS_EN = [
    {
        'id': 1,
        'text': u'When Sebastian Thrun started working on self-driving cars at '
                u'Google in 2007, few people outside of the company took him '
                u'seriously. “I can tell you very senior CEOs of major American '
                u'car companies would shake my hand and turn away because I wasn’t '
                u'worth talking to,” said Thrun, now the co-founder and CEO of '
                u'online higher education startup Udacity, in an interview with '
                u'Recode earlier this week.',
        'relations': [('Sebastian Thrun', 'started working', 'Google', '2007'),
                      ('Thrun', 'CEO of', 'Udacity', 'now')]
    },

    {
        'id': 2,
        'text': u'Hillary Clinton met secretly with Barak Obama last week.',
        'relations': [('Hillary Clinton', 'met', 'Barak Obama', 'last week')]
    },
    {
        'id': 3,
        'text': u'Donald Trump had a debate with Barak Hussein Obama and Hillary Clinton last Tuesday.',
        'relations': [('Donald Trump', 'debate', 'Barak Hussein Obama', 'last Tuesday'),
                      ('Donald Trump', 'debate', 'Hillary Clinton', 'last Tuesday')]
    },

    {
        'id': 4,
        'text': u'Last week Hillary, mother of Chelsea and Dan, met with congressman Mike Pence in the White House.',
        'relations': [('Hillary', 'met', 'Mike Pence', 'Last week'),
                      ('Hillary', 'mother of', 'Chelsea', None),
                      ('Hillary', 'mother of', 'Dan', None)]
    },
    {
        'id': 5,
        'text': u'Mark Zuckerberg, CEO of Facebook, gave testimony to the U.S. Senate Sunday morning.',
        'relations': [('Mark Zuckerberg', 'gave testimony', 'the U.S. Senate', 'Sunday morning'),
                      ('Mark Zuckerberg', 'CEO of', 'Facebook', None)]
    },

    {
        'id': 6,
        'text': u'Hillery killed David.',
        'relations': [('Hillery', 'killed', 'David', None)]
    },

    {
        'id': 7,
        'text': u'David killed by Hillery.',
        'relations': [('David', 'killed by', 'Hillery', None)]
    },

    # is_a / is_the / is_not / did_not
    {
        'id': 8,
        'text': u'Bill is the president of the U.S.',
        'relations': [('Bill', 'president', 'U.S.', None)]
    },
    {
        'id': 9,
        'text': u'George Washington was the first president of the U.S.',
        'relations': [('George Washington', 'first president', 'U.S.', None)]
    },
    {
        'id': 10,
        'text': u'Hillery is the biologic mother of Chelsea.',
        'relations': [('Hillery', 'biologic mother', 'Chelsea', None)]
    },
    {
        'id': 11,
        'text': u'Hillery is the step mother of Chelsea.',
        'relations': [('Hillery', 'step mother', 'Chelsea', None)]
    },
    {
        'id': 12,
        'text': u'Hillery is not the mother of Bill.',
        'relations': []
    },
    {
        'id': 13,
        'text': u'Hillery did not meet with Bill.',
        'relations': []
    },
    {
        'id': 14,
        'text': u'Bill and Hillery Clinton, parents of Chelsea married on October 11, 1975.',
        'relations': [('Bill', 'married', None, 'October 11, 1975'),
                      ('Hillery Clinton', 'married', None, 'October 11, 1975')]
    },
    {
        'id': 15,
        'text': u'Bill and Hillery Clinton, Chelsea parents, married on October 11, 1975.',
        'relations': [('Bill', 'married', None, 'October 11, 1975'),
                      ('Hillery Clinton', 'married', None, 'October 11, 1975')]
    },
    {
        'id': 16,
        'text': u'Bill and Hillery Clinton married on October 11, 1975.',
        'relations': [('Bill', 'married', None, 'October 11, 1975'),
                      ('Hillery Clinton', 'married', None, 'October 11, 1975')]
    },
]
