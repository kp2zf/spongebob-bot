import os
import logging
import slack
import ssl as ssl_lib
import certifi
from slackbotpython import SlackbotPython

# For simplicity we'll store our app data in-memory with the following data structure.
# slackbotpython_sent = {"channel": {"user_id": SlackbotPython}}
slackbotpython_sent = {}


def start_onboarding(web_client: slack.WebClient, user_id: str, channel: str):
    # Create a new onboarding tutorial.
    slackbotpython = SlackbotPython(channel)

    # Get the onboarding message payload
    message = slackbotpython.get_message_payload()

    # Post the onboarding message in Slack
    response = web_client.chat_postMessage(**message)

    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message after a user
    # has completed an onboarding task.
    slackbotpython.timestamp = response["ts"]

    # Store the message sent in slackbotpython_sent
    if channel not in slackbotpython_sent:
        slackbotpython_sent[channel] = {}
    slackbotpython_sent[channel][user_id] = slackbotpython


# ============= Reaction Added Events ============= #
# When a users adds an emoji reaction to the onboarding message,
# the type of the event will be 'reaction_added'.
# Here we'll link the update_emoji callback to the 'reaction_added' event.
@slack.RTMClient.run_on(event="reaction_added")
def update_emoji(**payload):
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data["item"]["channel"]
    user_id = data["user"]

    if channel_id not in slackbotpython_sent:
        return

    slackbotpython = slackbotpython_sent[channel_id][user_id]
    slackbotpython.reaction_task_completed = True
    message = slackbotpython.get_message_payload()
    updated_message = web_client.chat_update(**message)
    slackbotpython.timestamp = updated_message["ts"]
    
@slack.RTMClient.run_on(event="message")
def message(**payload):
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data.get("channel")
    user_id = data.get("user")
    text = data.get("text")

    if text and text.lower() == "start":
        return start_onboarding(web_client, user_id, channel_id)

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = os.environ["SLACK_BOT_TOKEN"]
    rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context)
    rtm_client.start()