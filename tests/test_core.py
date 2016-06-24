""" 
Core tests.
"""
def test_classification():
    """ 
    Tests classification using the example app.
    """
    import sys
    sys.path += '..'
    from talkback.core import App, Intent
    import yaml
    
    # Setup
    app = App('TestClassificationApp')
    config_file = file('examples/telco/talkback.yml','r')
    config_data = yaml.safe_load(config_file)
    app_data = config_data['Apps'][0]['App'] # the telco app
    for intent_config_data in app_data['Intents']:
        intent = Intent(intent_config_data)
        app[intent.name] = intent
    
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

