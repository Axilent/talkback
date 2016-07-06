""" 
Intents for Telco
"""
from talkback.core import Options, Option, user_cancel, terminate, Interview, IntentHelper

class SeeBalance(IntentHelper):
    """ 
    See the account balance.
    """
    def invoke(self,session):
        """ 
        Invoker method for SeeBalance.
        """
        session.speak('Your balance is $89.54.')

class PayBill(IntentHelper):
    """ 
    Pay the bill.
    """
    def options(self):
        """ 
        Gets options associated with this intent.
        """
        return {'Pay Bill Now':Option('Pay Bill Now',self.pay_bill,2),
                'Cancel':Option('Cancel',user_cancel,1)}
    
    def invoke(self,session):
        """ 
        Invoker for pay bill.
        """
        media_file = file('examples/telco/resources/cave.png','rb')
        session.speak('Hi!',media=media_file)
        option_list = self.options().values()
        options = Options('Would you like to pay your bill now?',*option_list)
        session.speak('Your balance is $89.54. You can pay your bill with your credit card on file, ending with 3465.',options=options)
    
    def pay_bill(self,session):
        """ 
        Pays the bill.
        """
        print 'in pay bill function'
        # In reality, business logic to pay the bill goes here
        session.speak('Your bill has been paid!  Thank you!')

class AddFeature(IntentHelper):
    """ 
    Add a feature.
    """
    def invoke(self,session):
        """ 
        Invoker for Add Feature.
        """
        questions = [('What would you like to add to your account?',['Travel Minutes 100','Travel Minutes 500','Travel Data 5GB','Travel Data 20GB'])]
        interview = Interview(questions,'You can add a number of different features to your account, depending on your needs.')
        interview.conduct_interview(session)
        session.speak('OK.  You added %s to your account. Thanks!' % interview.answers['What would you like to add to your account?'])

class CheckUsage(IntentHelper):
    """ 
    Check phone usage.
    """
    def invoke(self,session):
        """ 
        Invoker for Check Usage.
        """
        session.speak('You have used 123 minutes this billing period, out of a total of 400 minutes.')

