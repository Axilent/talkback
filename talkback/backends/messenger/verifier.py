""" 
Verifies the app in order to set it up in Facebook. Run this server with

python -m talkback.backends.messenger.verifier

before running verification from the Facebook app panel.
"""
from flask import Flask, request
import os
import requests

app = Flask('messenger_webhook')

@app.route('/',methods=['GET'])
def handle_verification():
    """ 
    Handles Facebook verification call.
    """
    return request.args['hub.challenge']

if __name__ == '__main__':
    app.run(debug=True)

