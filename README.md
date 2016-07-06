# Talkback

> A declarative framework for chatbots and voice agent skills.

The Talkback framework allows you to create chatbots and voice agent skills. Using a declarative syntax, you can define apps that interact with conversational interfaces. The framework will provide integration with popular platforms, and provide built-in natural language processing.

## Target Platforms

### Voice Agents

* Amazon Alexa
* Microsoft Cortina
* Apple Siri
* Google Home

### Messaging Platforms

* Facebook Messenger
* Slack
* Skype
* iMessage

## Core Concepts

### Intents

A *Talkback* app consists of one or more **Intents**. An Intent represents a user goal - something a user is attempting to accomplish. The developer can define any number of phrases that indicate the Intent, in an Intent Map that accompanies the Intent. *Talkback* will train it's built-in natural language processor (NLP) with the phrases in the Intent Map.

### Sessions

When an Intent is invoked, it is passed a **Session**. A Session represents the specific interaction with the conversational platform. The business logic of the Intent communicates with the user via the Session.

A Session can have associated Metadata, which can inform the Intent to particulars about the interaction.

A Session has several built-in methods of interaction that an Intent can use to communicate with the user:

* An **Interview** is a set of one or more questions sent to the user, for which their answers are collected. It can be thought of as analgeous to a form on a web or mobile app. The user will experience the Interview as a series of questions asked by the conversational interface.
* An Intent may use a Session to simply **Speak** to the user. This can be in the form of text or audio (depending on the underlying platform), or may in some cases allow the attachment of a media file like an image.
* An Interview question or Speaking may be accompanied by **Options**: pre-defined choices for the user that directly trigger action.

## Example Code

	from talkback.core import Intent
	
	class PayBill(Intent):
	    """User wants to pay their phone bill."""
	    def invoke(self,session):
	        user_id = session.meta['user_id']
	        total = get_bill_total(user_id)
	        pay_options = PayOptions(user_id)
	        session.speak("You're balance is %f. Do you want to pay your bill?" % total,options=pay_options)



