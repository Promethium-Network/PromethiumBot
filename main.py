# Name: PromethiumBot.py
# Date: 7-20-23
# Author: Shradinx
# --------------------------------------

'''
##############################
CHECK ENV FILE FOR TOKEN PRIOR TO STARTING BOT
##############################
'''

# Import modules
import interactions
from interactions import Client, Intents, listen, slash_command, SlashContext, Embed, EmbedField, EmbedFooter, EmbedAuthor, EmbedAttachment, slash_option, OptionType, SlashCommandChoice, Task, IntervalTrigger
from datetime import datetime
from datetime import timezone
from dotenv import load_dotenv
import os
import requests
from pydantic import BaseModel
load_dotenv()

# Define activity status
activity = interactions.Activity.create(
    name="play.promethium-network.net",
    type=interactions.ActivityType.PLAYING,
)

extensions = [
    "serverembeds",
    "serverstatusembeds",
    "transcriptforwarder",
    "welcomemessage",
    "skillstats",
    "sand",
    "blockhuntstats",
]

# Define bot client, along with intents and display activity status
bot = Client(intents=Intents.DEFAULT |
             Intents.MESSAGE_CONTENT | Intents.GUILD_MEMBERS | Intents.GUILD_MESSAGES, activity=activity)


async def reload_blockhunt():
    bot.reload_extension("blockhuntstats")
    bot.reload_extension("skillstats")
    print("blockhuntstats Reloaded!")
    print("skillstats Reloaded!")


@listen()
async def on_ready():
    print("PromethiumBot Online!")
    task = Task(reload_blockhunt, IntervalTrigger(minutes=5))
    task.start()

# Load extensions
for ext in extensions:
    bot.load_extension(ext)
    print(f"{ext} Loaded!")

# Start PromethiumBot
bot.start(os.environ.get("TOKEN"))
