CORPUS_ES = [
    # OK
    {
        'id': 2,
        'text': 'Hillary Clinton se reunió en secreto con Barack Obama la semana pasada.',
        'relations': [('Hillary Clinton', 'reunió', 'Barack Obama', 'la semana pasada')]
    },
    # {
    #     'id': 3,
    #     'text': 'Donald Trump debate con Barack Obama y Hillary Clinton el martes pasado.',
    #     'relations': [('Donald Trump', 'debate', 'Barack Obama', 'el martes pasado')]
    # },

    # {
    #     'id': 8,
    #     'text': 'Bill Clinton es el presidente de los U.S.A',
    #     'relations': [('Bill Clinton', 'presidente', 'U.S.A', None)]
    # },

    # FIX
    # 'Last week Hillary, mother of Chelsea, met with congressman Mike Pence in the White House.'
    # {
    #     'id': 4,
    #     'text': 'La semana pasada, Hillery Clinton, madre de Chelsea Clinton, se reunió con el congresista Mike Pence en la Casa Blanca.',
    #     'relations': [('Hillary Clinton', 'conoció', 'Mike Pence'),
    #                   ('Hillary Clinton', 'madre de', 'Chelsea Clinton')]
    # },

    # FIX(*)
    # 'Mark Zuckerberg, CEO de Facebook, dio su testimonio al Senado de los Estados Unidos el domingo por la mañana.',
    # OK
    # 'Bill Gates, CEO de Microsoft.'
    # 'Mark Zuckerberg es el CEO de Facebook.'

    # FIX(Hillery Clinton -> Hillery)
    # 'Hillery Clinton mató a David',
    # FIX(*)
    # 'David asesinado por Hillery Clinton',

    # FIX
    # 'Hillery Clinton no se encontró con Bill Clinton',
    # 'Hillery Clinton es la madre biológica de Chelsea Clinton',
    # 'Hillery Clinton es la madrastra de Chelsea Clinton',
    # 'Hillery Clinton no es la madre de Bill Clinton',
]
