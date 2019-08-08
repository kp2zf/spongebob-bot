# Kush Patel, Summer 2019 SWE Intern

from flask import Flask, request
from threading import Thread
import json, os, slack, requests, redis

slack_token = os.environ["SLACK_API_TOKEN"]
client = slack.WebClient(token=slack_token)
# red = redis.Redis('localhost')
redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
red = redis.from_url(redis_url)
message_dict = "message_history"

app = Flask(__name__)
message = False

@app.route('/', methods=['GET', 'POST'])
def response():
    try:
        print("*** REQUEST RECEIVED ***")
        body = json.loads(request.data)
        if body['type'] == 'url_verification':
           return challenge_handler(body)
        elif body['type'] == 'event_callback':
            if body['event']['type'] == "reaction_added":
                if body['event']['reaction'] == 'mocking_spongebob':
                    if body['event']['item']['type'] == "message":
                        initialize_redis()
                        message = getMessage(body)
                        if message:
                            return reply_with_bot(message, body)
        return ""
    except Exception as e:
        return ("error:" + str(e), 400)

def getMessage(body):
    try:
        message_body = make_request_for_message_history(body)
        return is_new_message(body, message_body)
    except Exception as e:
        print(e)

def reply_with_bot(message_text, body):
    try:
        message = create_mocking_string(message_text)
        client.chat_postMessage(
         channel = body["event"]["item"]["channel"],
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

def make_request_for_message_history(body):
        channel_history_url = "https://slack.com/api/channels.history"
        message_channel = body["event"]["item"]["channel"]
        current_ts = float(body["event"]["event_ts"])
        one_hour_messages = current_ts - 3600
        payload = {
                'token': slack_token, 
                'channel': message_channel, 
                'oldest': one_hour_messages
            }
        r = requests.get(channel_history_url, params=payload)
        message_body = r.json()
        return message_body

def is_new_message(body, message_body):
    message_ts = float(body["event"]["item"]["ts"])
    for x in message_body["messages"]:
        if(float(x["ts"]) == message_ts and red.hincrby(message_dict, x["client_msg_id"]) == 1):
            red.hmset(message_dict, {"test_var": "test"})
            return x["text"]
    return False

def initialize_redis():
    red.hmset(message_dict, {"var": "initialize"})

def challenge_handler(body):
    print("*** CHALLEGE REQUEST HANDLED***")
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