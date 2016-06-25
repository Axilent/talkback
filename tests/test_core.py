""" 
Core tests.
"""
import sys
sys.path += '..'
from talkback.core import App, Intent
from talkback import dispatcher
import yaml
import pytest

@pytest.fixture
def get_app():
    """ 
    Sets up the app.
    """
    # Setup
    app = App('TestClassificationApp')
    config_file = file('examples/telco/talkback.yml','r')
    config_data = yaml.safe_load(config_file)
    app_data = config_data['Apps'][0]['App'] # the telco app
    for intent_config_data in app_data['Intents']:
        intent = Intent(intent_config_data)
        app[intent.name] = intent
    return app

def test_classification():
    """ 
    Tests classification using the example app.
    """
    app = get_app()
    
    # Test classification
    assert app.intent_for('Pay my bill').name == 'Pay Bill'
    assert app.intent_for('Billing').name == 'Pay Bill'
    assert app.intent_for('Pay').name == 'Pay Bill'
    
    assert app.intent_for('Add data plan').name == 'Add Feature'
    assert app.intent_for('Upgrade').name == 'Add Feature'
    assert app.intent_for('Add Minutes').name == 'Add Feature'
    
    assert app.intent_for('Check usage').name == 'Check Usage'
    assert app.intent_for('How many minutes have I used').name == 'Check Usage'
    assert app.intent_for('How much time have I used').name == 'Check Usage'

    assert app.intent_for('How much money do I owe?').name == 'See Balance'
    assert app.intent_for('How much do I owe?').name == 'See Balance'
    assert app.intent_for('How much is my next bill?').name == 'See Balance'

@pytest.fixture
def init_dispatcher():
    """ 
    Initializes the dispatcher.
    """
    dispatcher.init('examples/telco/talkback.yml')

def test_dispatcher_get_intent():
    """ 
    Tests the dispatcher.
    """
    init_dispatcher()
    
    assert dispatcher.get_intent('Telco','Pay Bill').name == 'Pay Bill'
    assert dispatcher.get_intent('Telco','Add Feature').name == 'Add Feature'
    assert dispatcher.get_intent('Telco','Check Usage').name == 'Check Usage'
    assert dispatcher.get_intent('Telco','See Balance').name == 'See Balance'
    
def test_dispatcher_intent_for():
    """ 
    Tests the intent for method of the dispatcher.
    """
    init_dispatcher()
    
    assert dispatcher.intent_for('Telco','Pay my bill').name == 'Pay Bill'
    assert dispatcher.intent_for('Telco','Billing').name == 'Pay Bill'
    assert dispatcher.intent_for('Telco','Pay').name == 'Pay Bill'
    
    assert dispatcher.intent_for('Telco','Add data plan').name == 'Add Feature'
    assert dispatcher.intent_for('Telco','Upgrade').name == 'Add Feature'
    assert dispatcher.intent_for('Telco','Add Minutes').name == 'Add Feature'
    
    assert dispatcher.intent_for('Telco','Check usage').name == 'Check Usage'
    assert dispatcher.intent_for('Telco','How many minutes have I used').name == 'Check Usage'
    assert dispatcher.intent_for('Telco','How much time have I used').name == 'Check Usage'
    
    assert dispatcher.intent_for('Telco','How much money do I owe').name == 'See Balance'
    assert dispatcher.intent_for('Telco','How much do I owe').name == 'See Balance'
    assert dispatcher.intent_for('Telco','How much is my next bill').name == 'See Balance'

    