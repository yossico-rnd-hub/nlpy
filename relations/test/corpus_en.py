CORPUS_EN = [
    {'text': 'Hillary Clinton met secretly with Barak Obama last week.',
        'relations': [('Hillary Clinton', 'met', 'Barak Obama', 'last week')]},
    {'text': 'Donald Trump debate with Barak Obama and Hillary Clinton last Tuesday.',
        'relations': [('Donald Trump', 'debate', 'Barak Obama', 'last Tuesday'),
                      ('Donald Trump', 'debate', 'Hillary Clinton', 'last Tuesday')]},

    {'text': 'Bill is the president of the U.S.',
        'relations': [('Bill', 'president', 'U.S.', None)]},
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

    {'text': 'Hillery did not meet with Bill.',
        'relations': []},
    {'text': 'Hillery is the biologic mother of Chelsea.',
        'relations': [('Hillery', 'mother', 'Chelsea', None)]},
    {'text': 'Hillery is the step mother of Chelsea.',
        'relations': [('Hillery', 'step mother', 'Chelsea', None)]},
    {'text': 'Hillery is not the mother of Bill.',
        'relations': []},
]
