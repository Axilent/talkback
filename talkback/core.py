""" 
Core Talkback classes.
"""
from UserDict import DictMixin
from talkback.utils import gf
from textblob.classifiers import NaiveBayesClassifier as Classifier # TODO is this the right choice?
import yaml
from types import TupleType, StringType
from threading import local as threadlocal

class Session(object):
    """ 
    A session provides a connection from a Talkback app to a user.
    """
    def __init__(self,backend):
        self.backend = backend
    
    @property
    def id(self):
        """ 
        Gets the session id. Supplied by the backend.
        """
        return self.backend.get_id()
    
    def speak(self,message,options=None,media=None):
        """ 
        Speaks to the user.
        """
        self.backend.speak(self,message,options=options,media=media)
    
    def interview_user(self,interview):
        """ 
        Executes an interview with the user.
        """
        backend.interview_user(interview)
        return interview

class Termination(Exception):
    """ 
    Terminates the session.
    """

def terminate(session):
    """ 
    Causes the session to terminate.
    """
    raise Termination()

class UserCancellation(Termination):
    """ 
    Indicates the user cancels an operation.
    """

def user_cancel(session):
    """ 
    A user cancels an operation.
    """
    raise UserCancellation()

class BackendException(Exception):
    """ 
    Indicates a problem or limitation with a backend.
    """

class Interview(object):
    """ 
    An interview questions a user and collects answers.
    
    The questions is an interable, and can container either strings
    or 2-tuples of strings and a list of multiple choice answers.
    """
    def __init__(self,questions,introduction=None):
        self.questions = questions
        self.answers = {}
        self.introduction = introduction
    
    def conduct_interview(self,session):
        """ 
        Conducts the interview with the user.
        """
        if self.introduction:
            session.speak(self.introduction)
        
        for question in self.questions:
            if type(question) is TupleType:
                self.ask_multiple_choice_question(session,question)
            elif type(question) is StringType:
                self.ask_question(session,question)
            else:
                raise ValueError('Bad question:%s' % str(question))
    
    def set_answer(self,question,answer):
        """ 
        Sets an answer.
        """
        self.answers[question] = answer
    
    def ask_multiple_choice_question(self,session,question):
        """ 
        Asks a question with options.
        """
        question_text, possible_answers = question
        option_list = [SetAnswerOption(possible_answer,question_text,self) for possible_answer in possible_answers]
        options = Options('Please choose an option:',*option_list)
        
        session.speak(question_text,options=options)
    
    def ask_question(self,session,question):
        """ 
        Asks a simple question.
        """
        session.speak(question)
        answer = session.listen()
        self.set_answer(question,answer)

class Option(object):
    """ 
    An option for a user.
    """
    def __init__(self,label,callback,priority=1):
        self.label = label
        self.callback = callback
        self.priority = priority
    
    def __cmp__(self,other):
        if self.priority == other.priority:
            return cmp(self.label,other.label)
        else:
            return cmp(self.priority,other.priority)

class SetAnswerOption(Option):
    """ 
    An option that specifically sets an answer for an interview.
    """
    def __init__(self,label,question,interview,priority=1):
        super(SetAnswerOption,self).__init__(label,self.set_answer,priority=priority)
        self.question = question
        self.interview = interview
    
    def set_answer(self,session):
        """ 
        Sets the answer for the question, on the interview.
        """
        self.interview.set_answer(self.question,self.label)

class Options(object):
    """ 
    Options are represented as a multiple choice decision to be made
    by the user.
    """
    def __init__(self,call_to_action,*options_list):
        self.call_to_action = call_to_action
        self.options = {}
        for option in options_list:
            self.options[option.label] = option
        self.options_list = list(options_list)
        self.options_list.sort(reverse=True)
    
    def __len__(self):
        return len(self.options_list)

class IntentHelper(object):
    """ 
    Convenience superclass for intent helpers.
    """
    def options(self):
        """ 
        Returns empty dictionary. Subclasses override.
        """
        return {}
    
    def invoke(self,session):
        """ 
        Subclasses override.
        """
        raise NotImplemented()

class Intent(object):
    """ 
    An intent represents a user goal, and serves as an entry point into
    a Talkback app.
    """
    def __init__(self,config_data):
        self.name = config_data['Intent']['name']
        self.helper = gf(config_data['Intent']['code'])()
        self.phrases = config_data['Intent']['phrases']
    
    def invoke(self,session):
        """ 
        Mainline for the intent. Called by the dispatcher, and supplying the
        user session.
        """
        self.helper.invoke(session)
    
    def options(self):
        """ 
        Gets options associated with the intent.
        """
        return self.helper.options()

_local_intent = threadlocal()

class intention(object):
    """ 
    Context manager for setting an intent in the threadlocal.
    """
    def __init__(self,intent):
        self.intent = intent
    
    def __enter__(self):
        _local_intent.intent = self.intent
    
    def __exit__(self,*args):
        _local_intent.intent = None

def get_intention():
    """ 
    Gets the intention set in the thread local.
    """
    return _local_intent.intent

class IntentNotFound(Exception):
    """ 
    An error indicating a specified intent was not found.
    """

class AppNotFound(Exception):
    """ 
    An error indicating a specified app was not found.
    """

class App(DictMixin):
    """ 
    Aggregation of intents.
    """
    def __init__(self,name,greeting):
        self.name = name
        self.greeting = greeting
        self.intents = {}
        self.classifier = None
    
    def __getitem__(self,key):
        return self.intents[key]
    
    def __setitem__(self,key,value):
        self.intents[key] = value
        
        # train classifier
        phrase_file = file(value.phrases,'r')
        phrase_data = yaml.safe_load(phrase_file)
        phrases = [(phrase,value.name) for phrase in phrase_data['Phrases']]
        
        if self.classifier:
            self.classifier.update(phrases)
        else:
            self.classifier = Classifier(phrases)
    
    def __delitem__(self,key):
        del self.intents[key]
    
    def keys(self):
        return self.intents.keys()
    
    def intent_for(self,phrase):
        """ 
        Attempt to match an intent to the supplied phrase, using the onboard classifier.
        """
        if not self.classifier:
            # has not been properly initializes
            raise IntentNotFound('Classifier not initialized')
        
        try:
            return self.intents[self.classifier.classify(phrase)]
        except KeyError:
            raise IntentNotFound

