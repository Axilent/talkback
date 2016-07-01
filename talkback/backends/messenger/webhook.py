""" 
Webhook for Facebook Messenger.
"""
from flask import Flask, request, send_file
import os
import requests
from talkback import dispatcher, Session, Termination, get_intention, intention, UserCancellation, BackendException
from talkback import media as media_storage
import logging

app = Flask('messenger_webhook')

ACCESS_TOKEN = os.environ.get('MESSENGER_ACCESS_TOKEN','')
FB_GRAPH_ENDPOINT = 'https://graph.facebook.com/v2.6/me/messages?access_token='+ACCESS_TOKEN

MESSENGER_DEBUG = True if os.environ.get('MESSENGER_DEBUG',None) else False

MEDIA_HOST = os.environ.get('MESSENGER_MEDIA_HOST','')

log = logging.getLogger('talkback')

# Initialize the talkback app

def reply(user_id,msg,options=None,media=None):
    """ 
    Replies to the user.
    """
    if options and media:
        raise BackendException('Facebook Messenger API can only handle options (structured message) or media, but not both in the same message.')
    
    data = None
    if options:
        button_list = []
        for option in options.options_list:
            button = {
                'type':'postback',
                'title':option.label,
                'payload':'%s:%s' % (get_intention().name,option.label),
            }
            button_list.append(button)
        
        attachment = {
            'type':'template',
            'payload':{
                'template_type':'button',
                'text':'%s %s' % (msg,options.call_to_action),
                'buttons':button_list
            }
        }
        data = {
            'recipient':{'id':user_id},
            'message':{'attachment':attachment}
        }
    elif media:
        if not MEDIA_HOST:
            raise BackendException('Must set MESSENGER_MEDIA_HOST to use media files.')
        
        filename = media_storage.set_file(media)
        media_url = '%s/media/%s' % (MEDIA_HOST,filename)
            
        attachment = {
            'type':'image',
            'payload':{'url':media_url}
        }
        data = {
            'recipient':{'id':user_id},
            'message':{'attachment':attachment}
        }
    else:
        data = {
            'recipient':{'id':user_id},
            'message':{'text':msg}
        }
        
    response = requests.post(FB_GRAPH_ENDPOINT,json=data)
    print response.content

@app.route('/',methods=['POST'])
def handle_incoming_messages():
    """ 
    Handles FB verification.
    """
    log.debug('incoming message from Facebook')
    dispatcher.init()
    talkback_app = dispatcher.get_default_app()
    from talkback.backends.messenger import MessengerSession
    session = None
    try:
        data = request.json
        log.debug('data is: %s' % unicode(data))
        sender = data['entry'][0]['messaging'][0]['sender']['id']
        if 'postback' in data['entry'][0]['messaging'][0]:
            postback = data['entry'][0]['messaging'][0]['postback']['payload']
            process_postback(talkback_app,sender,postback)
        else:
            message = data['entry'][0]['messaging'][0]['message']['text']
            intent = talkback_app.intent_for(message)
            with intention(intent):
                session = Session(MessengerSession(sender))
                intent.invoke(session)
                
    except KeyError:
        log.info('Messageless request from user %s' % sender)
    except Termination:
        log.info('Session terminated')
        if session:
            session.speak('Bye!')
    
    return 'ok'

@app.route('/media/<filename>')
def media_file(filename):
    """ 
    Retrieves a media file.
    """
    outfile = media_storage.get_file(filename)
    return send_file(outfile,mimetype='image/png')

def process_postback(talkback_app,sender,postback):
    """ 
    Processes the postback call.
    """
    from talkback.backends.messenger import MessengerSession
    intent_name, option_name = postback.split(':')
    intent = talkback_app[intent_name]
    session = None
    with intention(intent):
        try:
            option = intent.options()[option_name]
            session = Session(MessengerSession(sender))
            option.callback(session)
        except Termination:
            log.info('Session terminated.')
            if session:
                session.speak('Bye!')

def refresh_subscription():
    """ 
    Sends POST to graph endpont to refresh subscription on Facebook.
    """
    refresh_endpoint = 'https://graph.facebook.com/v2.6/me/subscribed_apps?access_token='+ACCESS_TOKEN
    response = requests.post(refresh_endpoint)
    return (response.status_code,response.text)

if __name__ == '__main__':
    app.run(debug=MESSENGER_DEBUG) # TODO switch debug flag
