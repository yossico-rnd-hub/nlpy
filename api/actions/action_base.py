from flask import Response


class Action(object):
    '''
    Base action for REST API
    '''

    def __init__(self, name='home', endpoint='/', action=None, methods=['GET']):
        self.name = name
        self.endpoint = endpoint
        self.action = action
        self.methods = methods
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        if (self.action):
            return self.action()
        return self.response
