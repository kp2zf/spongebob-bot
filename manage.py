from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def response():
    try:
        body = json.loads(request.data)
        print(body['type'])
        if body['type'] == 'url_verification':
           return challenge_handler(body)
        elif body['type'] == 'event_callback':
            return event_handler(body)
        else:
            raise Exception("Error: Incorrect Type")
    except Exception as e:
        return ("error:" + str(e), 400)

def event_handler(body):
    return create_mocking_string(body["event"]["text"])

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
