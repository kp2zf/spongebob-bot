from flask import Flask, request
# from slackclient import SlackClient

app = Flask(__name__)
# slack_client = SlackClient('SLACK_TOKEN')
# slack_client.api_call("api.test")

@app.route('/')
def response():
    phrase = request.args.get('key')
    new_phrase = create_mocking_string(phrase)
    return {'key': new_phrase }

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

@app.route('/challenge/')
def challenge():
    token = request.args.get('challenge')
    return {'challenge': token }