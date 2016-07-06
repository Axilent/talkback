""" 
This is a mock backend for testing. It is controlled by the `mocktalk` command.
"""
from talkback.core import Session, UserCancellation, Termination
import sys

class MockSession(object):
    """ 
    Mock version of a session helper.
    """
    def get_id(self):
        """ 
        Hardcoded as 'mockuser'.
        """
        return 'mockuser'
    
    def speak(self,session,message,options=None,media=None):
        """ 
        Speaks the message.
        """
        if media:
            print message,'(media file attached)'
        else:
            print message
        if options:
            while True:
                option_index = 1
                for option in options.options_list:
                    print option_index,option.label
                    option_index += 1
                user_cmd = raw_input('What would you like to do? ')
                selected_option = None
                try:
                    try:
                        selected_option_index = int(user_cmd)
                        if selected_option_index > 0 and selected_option_index <= len(options.options_list):
                            selected_option = options.options_list[selected_option_index-1]
                    except TypeError:
                        pass # not an integer
                
                    if not selected_option:
                        selected_option = options.options[user_cmd]
                
                    selected_option.callback(session)
                    return
                except KeyError:
                    print 'Sorry I don\'t understand.'
                    print '--------------------------'
                except UserCancellation:
                    print 'Bye!'
                    sys.exit(0)
                except Termination:
                    sys.exit(0)
    
    def interview(self,interview):
        """ 
        Conducts interview.
        """
        pass # TODO

