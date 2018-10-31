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
        'relations': [('Sebastian Thrun', 'started working', 'Google', '2007', 'x:en-svo'),
                      ('Thrun', 'CEO of', 'Udacity', 'now', 'x:prep-rel')]
    },

    {
        'id': 2,
        'text': u'Hillary Clinton met secretly with Barak Obama last week.',
        'relations': [('Hillery Clinton', 'met', 'Barak Obama', 'last week', 'x:en-svo')]
    },

    {
        'id': 3,
        'text': u'Donald Trump had a debate with Barak Hussein Obama and Hillary Clinton last Tuesday.',
        'relations': [('Donald Trump', 'debate', 'Barak Hussein Obama', 'last Tuesday', 'x:en-svo'),
                      ('Donald Trump', 'debate', 'Hillary Clinton', 'last Tuesday', 'x:en-svo')]
    },

    {
        'id': 4,
        'text': u'Last week Hillary, mother of Chelsea and Dan, met with congressman Mike Pence in the White House.',
        'relations': [('Hillary', 'met', 'Mike Pence', 'Last week', 'x:en-svo'),
                      ('Hillary', 'mother of', 'Chelsea', None, 'x:prep-rel'),
                      ('Hillary', 'mother of', 'Dan', None, 'x:prep-rel')]
    },

    {
        'id': 5,
        'text': u'Mark Zuckerberg, CEO of Facebook, gave testimony to the U.S. Senate Sunday morning.',
        'relations': [('Mark Zuckerberg', 'gave testimony', 'the U.S. Senate', 'Sunday morning', 'x:en-svo'),
                      ('Mark Zuckerberg', 'CEO of', 'Facebook', None, 'x:prep-rel')]
    },

    {
        'id': 6,
        'text': u'Hillary killed David.',
        'relations': [('Hillary', 'killed', 'David', None, 'x:en-svo')]
    },

    {
        'id': 7,
        'text': u'David killed by Hillary.',
        'relations': [('David', 'killed by', 'Hillary', None, 'x:en-svo')]
    },

    {
        'id': 8,
        'text': u'Bill is the president of the U.S.',
        'relations': [('Bill', 'president', 'U.S.', None, 'x:en-svo')]
    },

    {
        'id': 9,
        'text': u'George Washington was the first president of the U.S.',
        'relations': [('George Washington', 'first president', 'U.S.', None, 'x:en-svo')]
    },

    {
        'id': 10,
        'text': u'Hillary is the biologic mother of Chelsea.',
        'relations': [('Hillary', 'biologic mother', 'Chelsea', None, 'x:en-svo')]
    },

    {
        'id': 11,
        'text': u'Hillary is the step mother of Chelsea.',
        'relations': [('Hillary', 'step mother', 'Chelsea', None, 'x:en-svo')]
    },

    {
        'id': 12,
        'text': u'Hillary is not the mother of Bill.',
        'relations': []
    },

    {
        'id': 13,
        'text': u'Hillary did not meet with Bill.',
        'relations': []
    },

    {
        'id': 14,
        'text': u'Bill and Hillary Clinton, parents of Chelsea married on October 11, 1975.',
        'relations': [('Bill', 'married', None, 'October 11, 1975', 'x:en-relcl-v-o'),
                      ('Hillary Clinton', 'married', None, 'October 11, 1975', 'x:en-relcl-v-o'),
                      ('Bill', 'married', 'Hillary Clinton', 'October 11, 1975'),
                      ('Bill', 'parents of', 'Chelsea', None, 'x:prep-rel'),
                      ('Hillary Clinton', 'parents of', 'Chelsea', None, 'x:prep-rel')]
    },

    # lilo (15): Hillary -> Hillery
    {
        'id': 15,
        'text': u'Bill and Hillery Clinton, Chelsea parents, married on October 11, 1975.',
        'relations': [('Bill', 'married', None, 'October 11, 1975', 'x:en-svo'),
                      ('Hillery Clinton', 'married', None, 'October 11, 1975', 'x:en-svo')]
    },

    {
        'id': 16,
        'text': u'Bill and Hillary Clinton married on October 11, 1975.',
        'relations': [('Bill', 'married', None, 'October 11, 1975', 'x:en-svo'),
                      ('Hillary Clinton', 'married', None, 'October 11, 1975', 'x:en-svo')]
    },
]
