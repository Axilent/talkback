""" 
Main dispatcher for Talkback apps.
"""
import os
import yaml
from talkback.core import App, Intent, IntentNotFound, AppNotFound

class ConfigError(Exception):
    """ 
    Indicates a configuration problem with Talkback.
    """

def get_app(app_name):
    """ 
    Gets the specified app.
    """
    try:
        return app_map[app_name]
    except KeyError:
        raise AppNotFound("Can't find %s" % app_name)

def get_intent(app_name,intent_name):
    """ 
    Gets the intent by name.
    """
    try:
        return app_map[app_name][intent_name]
    except KeyError:
        raise IntentNotFound()

def intent_for(app_name,text):
    """ 
    Gets the intent that matches the specified text.
    """
    try:
        return app_map[app_name].intent_for(text)
    except KeyError:
        raise IntentNotFound()


app_map = {}

def init(config_path=None):
    """ 
    Initializes the Dispatcher. Relies on the TALKBACK_CONFIG envar.
    """
    config_file_path = config_path or os.environ.get('TALKBACK_CONFIG',None)
    if not config_file_path:
        raise ConfigError('No config file set. Define TALKBACK_CONFIG enviornment variable.')
    
    try:
        # ingest the config file
        config_file = file(config_file_path,'r')
        data = yaml.safe_load(config_file)
    
        for app_wrapper in data['Apps']:
            app_data = app_wrapper['App']
            app = App(app_data['Name'],app_data['Greeting'])
            for intent_wrapper in app_data['Intents']:
                intent = Intent(intent_wrapper)
                app[intent.name] = intent
            app_map[app.name] = app
    except Exception as e:
        raise ConfigError(e)
