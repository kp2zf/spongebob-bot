from flask import Flask, request
import json
import os
import slack

slack_token = os.environ["SLACK_API_TOKEN"]
client = slack.WebClient(token=slack_token)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def response():
    try:
        body = json.loads(request.data)
        print(body)
        if body['type'] == 'url_verification':
           return challenge_handler(body)
        elif body['type'] == 'event_callback':
            if body['event']['type'] == 'message' and body['event']['client_msg_id'] != None:
                return event_handler(body)
        else:
            raise Exception("Error: Incorrect Type")
    except Exception as e:
        return ("error:" + str(e), 400)

def event_handler(body):
    message = create_mocking_string(body["event"]["text"])
    client.chat_postMessage(
     channel="CLR24RLP9",
     blocks=[
	    {
		    "type": "section",
		    "text": {
		    	"type": "mrkdwn",
		    	"text": message
		    }
	    }
    ]
    )
    return message

def challenge_handler(body):
    return body["challenge"]

def create_mocking_string(phrase):
    new_phrase = ""
    for x, y in enumerate(phrase):
        new_phrase += alternate_case(x, y)
    return new_phrase

def alternate_case(x, y):
    if x % 2 == 0:
        return y.lower()
    else:
        return y.upper()
