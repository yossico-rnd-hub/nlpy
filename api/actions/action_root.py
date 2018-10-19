from datetime import datetime
from .action_base import Action


class Root(Action):
    '''
    API root
    '''
    def __init__(self):
        self.name = 'api_root'
        self.endpoint = '/'
        self.methods = ['GET']

    def __call__(self, *args):
        now = datetime.now()
        formatted_now = now.strftime("%A, %d %B, %Y at %X")
        return "nlpy service ready.<br>" + formatted_now, 200
