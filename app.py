"""FlipBot

A simple slack bot which just flips a coin. Will build something better than this later on.
"""

import os
import random

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
app = Flask(__name__)

slack_events_adapter = SlackEventAdapter(os.getenv("SLACK_EVENTS_TOKEN"), "/slack/events", app)

slack_web_client = WebClient(token=os.getenv("SLACKBOT_TOKEN"))

MESSAGE_BLOCK = {"type": "section", "text": {"type": "mrkdwn", "text": ""}}


@slack_events_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    text = event.get("text")
    if "flip a coin" in text.lower():
        channel_id = event.get("channel")
        rand_int = random.randint(0, 1)
        results = "Heads" if rand_int == 0 else "Tails"
        text_message = f"The result is {results}"

        MESSAGE_BLOCK["text"]["text"] = text_message
        message_to_send = {"channel": channel_id, "blocks": [MESSAGE_BLOCK]}

        return slack_web_client.chat_postMessage(**message_to_send)


if __name__ == "__main__":
    app.run()
