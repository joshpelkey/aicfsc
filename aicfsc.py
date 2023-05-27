# Import the necessary package import sys
import sys
import datetime
import random
import openai
from slack_sdk.webhook import WebhookClient
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
import subprocess
from urlextract import URLExtract

# these are my api keys and stuff, hidden from git
import keys

# home dir /home/name
home_dir = keys.home_dir

# you're path for image
img_path1 = keys.img_path1

# slack bot token
bot_token = keys.bot_token

# Authenticate with OpenAI using your API key
openai.api_key = keys.openai_api_key

# no args, post to prod
if len(sys.argv) < 2:
 
    print ("posting to prod")
    # ai_stories slack
    webhook_client = WebhookClient(
        "https://hooks.slack.com/services/" + keys.slack_ai_key
    )

#if --dev arg, post to my own channel
elif sys.argv[1] == "--dev":
    print ("posting to dev")

    # me slack
    webhook_client = WebhookClient(
        "https://hooks.slack.com/services/" + keys.slack_dev_key
    )

# you did something weird
else:
    print ("you provided args, but they don't work")
    sys.exit()

# variables for our book (ehm, post)
today = datetime.date.today()
target_date = datetime.date(2023, 9, 4)
num_days = (target_date - today).days
if num_days < 1:
    sys.exit()

year = 2023 - num_days


# Ask ChatGPT your question
chat_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[
        {"role": "system", "content": "You are a historian and author writing interesting notes to your students."},
        {"role": "user", "content": "Tell me an interesting fact about Clemson or Clemson Football that happened in the year " + str(year) + ". Make sure it is historically accurate and not fabricated. Use 150 words or less."}
    ],
    temperature=0.75
)

# Ask ChatGPT your question
coach_quote = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[
        {"role": "system", "content": "You are a college football coach and motivational speaker."},
        {"role": "user", "content": "Tell us something a college football coach would say. Make sure it is fabricated and do not attribute any author. Use exactly 20 words or less."}
    ],
    temperature=0.75
)

# Ask ChatGPT your question
random_fact = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[
        {"role": "system", "content": "You are a statistician and college football analyst."},
        {"role": "user", "content": "Tell us about a college football game where Clemson beat South Carolina. Make sure it is historically accurate. Use exactly 20 words or less."}
    ],
    temperature=0.75
)

# ask for a dalle prompt 1
dalle_chat_response1 = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[
        {"role": "user", "content": "Pick a random art style and create an image of a clemson football player wearing the number " + str(num_days) + " in an orange and purple jersey doing something completely random"},

    ],
    temperature=0.75
)


# print stuffs to check
print("---- dalle prompts ----")
print(dalle_chat_response1['choices'][0]['message'].get("content"))

# generate a dope DALL-E image
dalle_response1 = openai.Image.create(prompt=dalle_chat_response1['choices'][0]['message'].get("content"), size="256x256")
image_url1 = dalle_response1["data"][0]["url"]

# get the first image and store it on imgur
img_data1 = requests.get(image_url1).content
with open(home_dir  + img_path1, "wb") as handler:
    handler.write(img_data1)

imgur1 = subprocess.run(
    [home_dir + "/.local/bin/imgur-uploader", home_dir + img_path1],
    stdout=subprocess.PIPE,
)

extractor1 = URLExtract()
imgur_str1 = str(imgur1)
url1 = extractor1.find_urls(imgur_str1)

clean_url1 = url1[0][:-4]

with open(home_dir + img_path1, 'rb') as f:
    img1 = f.read()

# Send the response to the incoming Slack webhook
slack_response = webhook_client.send(
    text= str(num_days) + "days until Clemson FOOTBAW!!1",
    blocks=[
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": str(num_days) + " DAYS! :football: :clemson: :football:  CLEMSON FOOTBAW COUNTDOWN"
            },
        },
        {
            "type": "context",
            "elements": [
                {
                    "text": coach_quote['choices'][0]['message'].get("content") + " -- chatGPT",
                    "type": "mrkdwn",
                }
            ],
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": chat_response['choices'][0]['message'].get("content")},
        },
        {"type": "divider"},
        {
            "type": "image",
            "title": {
                "type": "plain_text",
                "text": random_fact['choices'][0]['message'].get("content"),
                "emoji": True,
            },
            "image_url": clean_url1,
            "alt_text": dalle_chat_response1['choices'][0]['message'].get("content"),
        },
    ],
)

print("---- chat response ----")
print(chat_response)

print("---- dalle responses ----")
print(dalle_response1)

print("---- cleanurl ----")
print(clean_url1)

print("---- slack responses ----")
print(slack_response)
