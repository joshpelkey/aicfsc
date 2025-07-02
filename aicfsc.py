# Import the necessary package import sys
import sys
import datetime
import random
import base64
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
target_date = datetime.date(2025, 8, 30)
num_days = (target_date - today).days
if num_days < 1:
    sys.exit()

year = 2025 - num_days

themes = [
    "Gnomes",
    "Artificial Intelligence",
    "Time Travel",
    "Space Exploration",
    "Dystopian Society",
    "Cyberpunk",
    "Virtual Reality",
    "Alien Invasion",
    "Post-Apocalyptic World",
    "Alternate History",
    "Superpowers",
    "Parallel Universes",
    "Robots and Androids",
    "Genetic Engineering",
    "Extraterrestrial Life",
    "Time Manipulation",
    "Mind Uploading",
    "Nanotechnology",
    "Cloning",
    "Steampunk",
    "Biopunk",
    "Magic and Sorcery",
    "Dragons",
    "Vampires",
    "Zombies",
    "Werewolves",
    "Wizards and Witches",
    "Telekinesis",
    "Telepathy",
    "Space Opera",
    "Galactic Empire",
    "Intergalactic War",
    "Cyborgs",
    "Future Technology",
    "Apocalyptic Event",
    "Alternate Dimensions",
    "Exoskeleton Suits",
    "Surreal Worlds",
    "Lost Civilizations",
    "Mythical Creatures",
    "Time Paradoxes",
    "Invisible Cloaks",
    "Energy Weapons",
    "Advanced Robotics",
    "Transhumanism",
    "Cosmic Horror",
    "Mecha",
    "Holographic Interfaces",
    "Post-Human Society",
    "Supernatural Powers",
    "Genetic Mutations",
    "Invisibility",
    "Nano-enhancements",
    "Love and romance",
    "Coming of age",
    "Overcoming adversity",
    "Self-discovery",
    "Friendship and loyalty",
    "Quest and adventure",
    "Good vs. evil",
    "Survival in a hostile environment",
    "Loss and grief",
    "Hope and redemption",
    "Identity and belonging",
    "Power and corruption",
    "Social injustice",
    "War and conflict",
    "Exploration of the unknown",
    "Fate and destiny",
    "Resilience and perseverance",
    "Sacrifice for a greater cause",
    "Betrayal and deception",
    "Nature and the environment",
    "Mystery and suspense",
    "Family secrets",
    "Legacy and inheritance",
    "Rebellion against authority",
    "Challenges of parenthood",
    "Philosophical exploration",
    "Mental health and coping",
    "Ethical dilemmas",
    "Psychological thriller",
    "Struggle for power",
    "Art and creativity",
    "Forbidden love",
    "Warriors and heroes",
    "Historical events and figures",
    "The search for truth",
    "Small-town secrets",
    "Transformation and metamorphosis",
    "Fame and its consequences"
]

chosen_themes = random.sample(themes, 2)


# Ask ChatGPT your question
chat_response = openai.chat.completions.create(
    model="gpt-4.1-mini", 
    messages=[
        {"role": "system", "content": "You are a college football historian and statistical genius. You specialize in the Clemson football team and know all of their season stats, players, coaches, and traditions."},
        {"role": "user", "content": "Write a historical fiction story based on the Clemson football program in year " 
            + str(year) + "."
            + "Make sure the names and games used are historically accurate but add in themes of " 
            + chosen_themes[0] + " and " + chosen_themes[1] + ". Use your imagination and make the story fun (it could be a short story, a poem, a song, etc). Use 150 words or less. Start your response with " 
            + str(num_days) + " ago in " + str(year) + "..."}
    ],
    temperature=1
)

# Ask ChatGPT your question
coach_quote = openai.chat.completions.create(
    model="gpt-4.1-mini", 
    messages=[
        {"role": "system", "content": "You are a college football coach and motivational speaker."},
        {"role": "user", "content": "Pick from a list of 100 human emotions. Tell us something a college football coach would say related to the emotion. Make it sound down home or southern in some way. Southern sayings are known for their use of metaphors, similies, and exaggerations. Can be deeply rooted in southern culture, agricultrual, or relgious in nature.  Make sure it is fabricated and do not attribute any author. Use exactly 20 words or less. Only return the quote. Do not return the emotion that was chosen."}
    ],
    temperature=1
)

# Ask ChatGPT your question
random_fact = openai.chat.completions.create(
    model="gpt-4.1-mini", 
    messages=[
        {"role": "system", "content": "You are a Clemson football fan who hates the University of South Carolina."},
        {"role": "user", "content": "Compare or contrast the University of South Carolina's football team to something bad that happened in " + str(year) + ". Make sure to cast the football team in a negative light. Refer to them as USCjr, rather than the University of South Carolina. Use exactly 20 words or less."}
    ],
    temperature=1
)

# ask for a dalle prompt 1
dalle_chat_response1 = openai.chat.completions.create(
    model="gpt-4.1-mini", 
    messages=[
        {"role": "system", "content": "You are an expert image prompt engineer. "
                                     "Your task is to create a concise and evocative prompt that captures the "
                                     "themes of the story." },

        {"role": "user", "content": "Generate a prompt, less than 100 words, for an image based on " + chat_response.choices[0].message.content +
                                     "---- Incorporate a clemson football player wearing the number " 
                                      + str(num_days) + " in an orange and purple Clemson Tigers football jersey. "
                                      "Incorporate the Clemson tiger paw logo, either on the football helmet or in the picture. "}
    ],
    temperature=1
)


# print stuffs to check
print("---- dalle prompts ----")
print(dalle_chat_response1.choices[0].message.content)

# generate a dope DALL-E image
print("---- generate image ----")
dalle_response1 = openai.responses.create(
        model="gpt-4.1-mini",
        input= dalle_chat_response1.choices[0].message.content,
        tools=[{"type": "image_generation"}],
)

# Save the image to a file
print("---- saving the file ----")
image_data = [
    output.result
    for output in dalle_response1.output
    if output.type == "image_generation_call"
]

if image_data:
    image_base64 = image_data[0]
    with open(home_dir + img_path1, "wb") as f:
        f.write(base64.b64decode(image_base64))

print("---- uploading to imgur ----")
# get the first image and store it on imgur
imgur1 = subprocess.run(
    [home_dir + "/.local/bin/imgur-uploader", home_dir + img_path1],
    stdout=subprocess.PIPE,
)

extractor = URLExtract()
imgur_str = str(imgur1)
urls = extractor.find_urls(imgur_str)
clean_url1 = urls[0][:-4]  # Remove trailing newline character

# Send the response to the incoming Slack webhook
print("---- sending to slack ----")
slack_response = webhook_client.send(
    text= str(num_days) + " days until Clemson FOOTBAW!!1",
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
                    "text": coach_quote.choices[0].message.content + " -- DaboGPT",
                    "type": "mrkdwn",
                }
            ],
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": chat_response.choices[0].message.content},
        },
        {"type": "divider"},
        {
            "type": "image",
            "title": {
                "type": "plain_text",
                "text": random_fact.choices[0].message.content,
                "emoji": True,
            },
            "image_url": clean_url1,
            "alt_text": dalle_chat_response1.choices[0].message.content,
        },
    ],
)

print("---- chat response ----")
print(chat_response)

print("---- cleanurl ----")
print(clean_url1)

print("---- slack responses ----")
print(slack_response)
