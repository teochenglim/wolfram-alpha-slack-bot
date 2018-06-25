import logging

import time
from slackclient import SlackClient

import requests
import xml.etree.ElementTree

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def echo(bot, message):
    r = requests.get("https://api.wolframalpha.com/v2/query", {
        'input': message,
        'appid': 'WOLFRAMALPHA-APPID-HERE'
    })

    e = xml.etree.ElementTree.fromstring(r.text.encode('utf-8').strip())

    result = []
    for plaintext in e.findall('.//plaintext'):
        if isinstance(plaintext.text, basestring):
            result.append(plaintext.text)
    if len(result) == 0:
        result = ["Sorry, I don't know that.."]
    if len(result) == 1:
        result.append("Sorry, I don't know that..")
    print(result)
    bot.rtm_send_message(CHANNEL_NAME, result[1])

BOT_TOKEN = "SLACK-APPID-HERE"
CHANNEL_NAME = "SLACK-CHANNEL-NAME-HERE"

def main():
    # Create the slackclient instance
    sc = SlackClient(BOT_TOKEN)

    # Connect to slack
    if sc.rtm_connect():
        # Send first message
        sc.rtm_send_message(CHANNEL_NAME, "I'm a bot, please talk to me!")

        while True:
            # Read latest messages
            for slack_message in sc.rtm_read():
                message = slack_message.get("text")
                user = slack_message.get("user")
                if not message or not user:
                    continue
                echo(sc, message)
            # Sleep for half a second
            time.sleep(1)

if __name__ == '__main__':
    main()

