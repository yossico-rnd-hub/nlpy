#!env/bin/python

import sys
sys.path.append('.')

from actions.action_base import Action
from flask import Flask


def add_action(action):
    app.add_url_rule(
        action.endpoint,
        action.name,
        action,
        methods=action.methods)


app = Flask(__name__)

for cls in Action.__subclasses__():
    add_action(cls())


if __name__ == '__main__':
    app.run()
