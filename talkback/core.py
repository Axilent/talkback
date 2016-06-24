""" 
Core Talkback classes.
"""
from UserDict import DictMixin
from talkback.utils import gf
from textblob.classifiers import NaiveBayesClassifier as Classifier # TODO is this the right choice?
import yaml

class Session(object):
    """ 
    A session provides a connection from a Talkback app to a user.
    """
    def __init__(self,backend):
        self.backend = backend
    
    def speak(self,message,options=None,media=None):
        """ 
        Speaks to the user.
        """
        backend.speak(message,options=options,media=media)
    
    def interview_user(self,interview):
        """ 
        Executes an interview with the user.
        """
        backend.interview_user(interview)
        return interview

class Interview(object):
    """ 
    An interview questions a user and collects answers.
    """
    def __init__(self,questions):
        self.questions = questions
        self.answers = {}

class Options(object):
    """ 
    Options are represented as a multiple choice decision to be made
    by the user.
    """
    def __init__(self,*options_list):
        self.options = options_list

class Intent(object):
    """ 
    An intent represents a user goal, and serves as an entry point into
    a Talkback app.
    """
    def __init__(self,config_data):
        self.name = config_data['Intent']['name']
        self.helper = gf(config_data['Intent']['code'])
        self.phrases = config_data['Intent']['phrases']
    
    def invoke(self,session):
        """ 
        Mainline for the intent. Called by the dispatcher, and supplying the
        user session.
        """
        self.helper.invoke(session)

class IntentNotFound(Exception):
    """ 
    An error indicating a specified intent was not found.
    """

class App(DictMixin):
    """ 
    Aggregation of intents.
    """
    def __init__(self,name):
        self.name = name
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

