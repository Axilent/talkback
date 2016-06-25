""" 
Intents for Telco
"""
from talkback import Options, Option, user_cancel, terminate, Interview

class SeeBalance(object):
    """ 
    See the account balance.
    """
    def invoke(self,session):
        """ 
        Invoker method for SeeBalance.
        """
        session.speak('Your balance is $89.54.')

class PayBill(object):
    """ 
    Pay the bill.
    """
    def invoke(self,session):
        """ 
        Invoker for pay bill.
        """
        options = Options(Option('Pay Bill Now',self.pay_bill,2),
                          Option('Cancel',user_cancel,1))
        session.speak('Your balance is $89.54. You can pay your bill with your credit card on file, ending with 3465.',options=options)
        terminate(session)
    
    def pay_bill(self,session):
        """ 
        Pays the bill.
        """
        # In reality, business logic to pay the bill goes here
        session.speak('Your bill has been paid!  Thank you!')
        terminate(session)

class AddFeature(object):
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
        terminate(session)

class CheckUsage(object):
    """ 
    Check phone usage.
    """
    def invoke(self,session):
        """ 
        Invoker for Check Usage.
        """
        session.speak('You have used 123 minutes this billing period.')
        terminate(session)

