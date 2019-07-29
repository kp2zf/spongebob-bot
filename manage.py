from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def response():
    # phrase = request.args.get('key')
    # new_phrase = create_mocking_string(phrase)
    # return {'key': new_phrase }
    try:
        body = json.loads(request.data)
        if body['type'] == 'challenge':
           return challange_handler(body)
        elif body['type'] == 'event_callback':
            return event_handler(body)
        else:
            raise Exception("Error: Incorrect Type")
    except Exception as e:
        return ("error:" + str(e), 400)

def event_handler(body):
    return body

def challange_handler(body):
    return {'challenge': body['challenge'] }

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
