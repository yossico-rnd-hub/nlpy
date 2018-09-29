CORPUS_ES = [
    # OK
    {
        'id': 2,
        'en': u'Hillary Clinton met secretly with Barak Obama last week.',
        'text': u'Hillary Clinton se reunió en secreto con Barack Obama la semana pasada.',
        'relations': [('Hillary Clinton', 'reunió', 'Barack Obama', None, 'x:es-svo')],
    },

    # FIX
    {
        'id': 3,
        'en': u'Donald Trump had a debate with Barak Hussein Obama and Hillary Clinton last Tuesday.',
        'text': u'Donald Trump debate con Barack Obama y Hillary Clinton el martes pasado.',
        'relations': [('Donald Trump', 'debate', 'Barack Obama', 'el martes pasado')],
    },

    # FIX
    {
        'id': 4,
        'en': u'Hillary Clinton, mother of Chelsea, met with congressman Mike Pence in the White House.',
        'text': u'Hillery Clinton, madre de Chelsea Clinton, se reunió con el congresista Mike Pence en la Casa Blanca.',
        'relations': [('Hillary Clinton', 'conoció', 'Mike Pence'),
                      ('Hillary Clinton', 'madre de', 'Chelsea Clinton')],
    },

    # FIX
    {
        'id': 5,
        'en': u'Mark Zuckerberg, CEO of Facebook, gave testimony to the U.S. Senate Sunday morning.',
        'text': u'Mark Zuckerberg, CEO de Facebook, dio su testimonio al Senado de los Estados Unidos el domingo por la mañana.',
        'relations': [('Mark Zuckerberg', 'dio su testimonio', 'de los Estados Unidos', 'el domingo por la mañana'),
                      ('Mark Zuckerberg', 'dio', 'Facebook')],
    },

    # OK
    {
        'id': 6,
        'en': u'Hillery killed David.',
        'text': u'Hillery Clinton mató a David.',
        'relations': [('Hillery Clinton', 'mató', 'David')],
    },

    # FIX
    {
        'id': 7,
        'en': u'David killed by Hillery.',
        'text': u'David asesinado por Hillery Clinton.',
        'relations': [('David', 'asesinado por', 'Hillery Clinton')],
    },

    # OK
    {
        'id': 8,
        'en': u'Bill is the president of the U.S.',
        'text': u'Bill Clinton es el presidente de los U.S.A',
        'relations': [('Bill Clinton', 'presidente', 'U.S.A', None, 'x:es-nsubj-noun-nmod')],
    },

    # OK
    {
        'id': 9,
        'en': u'George Washington was the first president of the U.S.',
        'text': u'George Washington fue el primer presidente de los Estados Unidos.',
        'relations': [('George Washington', 'primer presidente', 'los Estados Unidos', None, 'x:es-nsubj-noun-nmod')]
    },

    # OK
    {
        'id': 10,
        'en': u'Hillery is the biologic mother of Chelsea.',
        'text': u'Hillary es la madre biológica de Chelsea.',
        'relations': [('Hillary', 'madre biológica', 'Chelsea', None, 'x:es-nsubj-noun-nmod')]
    },

    # OK
    {
        'id': 11,
        'en': u'Hillery is the step mother of Chelsea.',
        'text': u'Hillery es la madrastra de Chelsea.',
        'relations': [('Hillery', 'madrastra', 'Chelsea', None, 'x:es-nsubj-noun-nmod')]
    },

    # OK
    {
        'id': 12,
        'en': u'Hillery is not the mother of Bill.',
        'text': u'Hillery no es la madre de Bill.',
        'relations': []
    },

    # OK
    {
        'id': 13,
        'en': u'Hillery did not meet with Bill.',
        'text': u'Hillery no se reunió con Bill.',
        'relations': []
    },

    # FIX
    {
        'id': 14,
        'en': u'Bill and Hillery Clinton, parents of Chelsea married on October 11, 1975.',
        'text': u'Bill y Hillary Clinton, padres de Chelsea se casaron el 11 de octubre de 1975.',
        'relations': [('Bill', 'casaron', None, 'October 11, 1975'),
                      ('Hillery Clinton', 'casaron', None, 'October 11, 1975'),
                      ('Bill', 'padres de', 'Chelsea', None),
                      ('Hillery Clinton', 'padres de', 'Chelsea', None)]
    },

    # FIX
    {
        'id': 15,
        'en': u'Bill and Hillery Clinton, Chelsea parents, married on October 11, 1975.',
        'text': u'Bill y Hillary Clinton, padres del Chelsea, se casaron el 11 de octubre de 1975.',
        'relations': [('Bill', 'casaron', None, 'October 11, 1975'),
                      ('Hillery Clinton', 'casaron', None, 'October 11, 1975')]
    },

    # FIX
    {
        'id': 16,
        'en': u'Bill and Hillery Clinton married on October 11, 1975.',
        'text': u'Bill y Hillary Clinton se casaron el 11 de octubre de 1975.',
        'relations': [('Bill', 'casaron', None, 'October 11, 1975'),
                      ('Hillery Clinton', 'casaron', None, 'October 11, 1975')]
    },
]