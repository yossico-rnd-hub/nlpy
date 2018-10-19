#!env/bin/python

from flask import Flask
from actions.action_base import Action


class NlpyServer(object):
    """Nlpy REST server"""

    def __init__(self):
        self.app = Flask(__name__)
        for cls in Action.__subclasses__():
            self.add_action(cls())

    def add_action(self, action):
        self.app.add_url_rule(
            action.endpoint,
            action.name,
            action,
            methods=action.methods)

    def run(self):
        self.app.run(debug=True)


if __name__ == '__main__':
    server = NlpyServer()
    server.run()
