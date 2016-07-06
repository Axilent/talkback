""" 
Intents for Telco
"""
from talkback.core import Options, Option, user_cancel, terminate, Interview, IntentHelper, SetAnswerOption

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
        #media_file = file('examples/telco/resources/cave.png','rb')
        #session.speak('Hi!',media=media_file)
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

account_question = 'What would you like to add to your account?'

class AddFeature(IntentHelper):
    """ 
    Add a feature.
    """
    def options(self):
        """ 
        Gets options for Add Feature.
        """
        return {
            'Travel Minutes 100':Option('Travel Minutes 100',self.travel_minutes_100,3),
            'Travel Data 5GB':Option('Travel Data 5GB',self.travel_data_5gb,2),
            'Travel Data 20GB':Option('Travel Data 20GB',self.travel_data_20gb,1)
        }
    
    def travel_minutes_100(self,session):
        """ 
        Adds travel minutes 100 package.
        """
        session.speak('Adding Travel Minutes 100 to your plan.')
    
    def travel_data_5gb(self,session):
        """ 
        Adds 5GB package to plan.
        """
        session.speak('Adding Travel Data 5GB to your plan.')
    
    def travel_data_20gb(self,session):
        """ 
        Adds 20GB data package to plan.
        """
        session.speak('Adding Travel Data 20GB to your plan.')
    
    def invoke(self,session):
        """ 
        Invoker for Add Feature.
        """
        option_list = self.options().values()
        options = Options('What would you like to add to your plan?',*option_list)
        session.speak('You can add a number of different features to your account, depending on your needs.',options=options)

class CheckUsage(IntentHelper):
    """ 
    Check phone usage.
    """
    def invoke(self,session):
        """ 
        Invoker for Check Usage.
        """
        session.speak('You have used 123 minutes this billing period, out of a total of 400 minutes.')

