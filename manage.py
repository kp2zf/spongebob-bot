from flask import Flask, request
import json
import os
import slack
import requests

slack_token = os.environ["SLACK_API_TOKEN"]
client = slack.WebClient(token=slack_token)

app = Flask(__name__)
emoji_count = 0

spongebob_mocked_messages = []

@app.route('/', methods=['GET', 'POST'])
def response():
    try:
        body = json.loads(request.data)
        if body['type'] == 'url_verification':
           return challenge_handler(body)
        elif body['type'] == 'event_callback':
            if body['event']['type'] == "reaction_added":
                if body['event']['reaction'] == 'grinning':
                    if body['event']['item']['type'] == "message":
                        message = getMessage(body)
                        if message:
                            return reply_with_bot(message)
        return ""
    except Exception as e:
        return ("error:" + str(e), 400)

def reply_with_bot(message_text):
    try:
        message = create_mocking_string(message_text)
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
        return ""
    except Exception as e:
        print(e)


def getMessage(body):
    try:
        channel_history_url = "https://slack.com/api/channels.history"
        message_channel = body["event"]["item"]["channel"]
        message_ts = float(body["event"]["item"]["ts"])
        five_min_messages = message_ts - 30000
        payload = {
                'token': slack_token, 
                'channel': message_channel, 
                'oldest': five_min_messages
            }
        r = requests.get(channel_history_url, params=payload)
        message_body = r.json()

        for x in message_body["messages"]:
            if(float(x["ts"]) == message_ts and x["client_msg_id"] not in spongebob_mocked_messages ):
                spongebob_mocked_messages.append(x["client_msg_id"])                 
                return x["text"]
        
        return False
    except Exception as e:
        print(e)

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
