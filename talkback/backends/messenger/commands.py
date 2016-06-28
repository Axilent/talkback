""" 
CLI commands for the messenger back end.
"""
from talkback.backends.messenger import webhook, verifier

def run_webhook():
    """ 
    Runs the webhook server.
    """
    webhook.app.run(debug=webhook.MESSENGER_DEBUG)

def run_verifier():
    """ 
    Runs the verifier server.
    """
    verifier.app.run(debug=True)

def run_refresh_subscription():
    """ 
    Refreshes subscription on Facebook by sending a POST.
    """
    return webhook.refresh_subscription()