""" 
Facebook Messenger backend.
"""
from talkback.backends.messenger.webhook import reply

class MessengerSession(object):
    """ 
    Session helper for Facebook Messenger.
    """
    def __init__(self,user_id):
        self.user_id = user_id
    
    def get_id(self):
        """ 
        Returns the Facebook id.
        """
        return self.user_id
    
    def speak(self,session,message,options=None,media=None):
        """ 
        Speaks the message. Media is a file object.
        """
        reply(self.user_id,message,options=options,media=media)

    def interview(self,interview):
        """ 
        Conducts interview.
        """
        pass # TODO
