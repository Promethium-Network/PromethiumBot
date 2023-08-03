# Name: PromethiumBot.py
# Date: 7-20-23
# Author: Shradinx
# --------------------------------------

'''
##############################
CHECK ENV FILE FOR TOKEN PRIOR TO STARTING BOT
##############################
'''

'''
	TODO: 
	- Finish server info embed
		= Add voting hyperlinks
'''

'''
Copy-Paste List:

[PromethiumMinecraft](https://patreon.com/PromethiumMinecraft)
You can join our in-game Minecraft server by connecting to play.promethium-network.net on 1.19.4 and above!
You can support our server by joining our Patreon, following our social medias, donating to our webstore, and voting for our server!
'''

# Import modules
import interactions
from interactions import Client, Intents, listen, slash_command, SlashContext, Embed, EmbedField, EmbedFooter, EmbedAuthor, EmbedAttachment, slash_option, OptionType, SlashCommandChoice
from datetime import datetime
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
    "transcriptForwarder",
    "welcomeMessage",
]

# Define bot client, along with intents and display activity status
bot = Client(intents=Intents.DEFAULT |
             Intents.MESSAGE_CONTENT | Intents.GUILD_MEMBERS | Intents.GUILD_MESSAGES, activity=activity)


@listen()
async def on_ready():
    print("PromethiumBot Online!")


@slash_command(
    name="serverinfo",
    description="Post the server info embed",
)
async def serverinfo(ctx: SlashContext):
    date = datetime.now().strftime("%x")

    # EmbedFields for networkinfo Embed
    aboutServer = EmbedField(
        name="About Promethium Network",
        value="Promethium Network is a Minecraft server network managed and owned by Shradinx and Gusbunce. "
        "\n \nIt was started in early July 2023 when Geographica, a previous Minecraft server, was announced to be shutting down."
        "\n  \nBelow, you can find other information about the server, such as links to our rules document and our social medias. \n \n"
    )
    joinInfo = EmbedField(
        name="\n How to join Promethium Network?",
        value="The in-game Minecraft server is currently not open the public. However when it is, you can join with play.promethium-network.net on versions 1.19.4 and above!"
        "\n \n It is recommended that you have **Resource Packs: Enabled** set prior to joining the server!"
    )
    howSupport = EmbedField(
        name="How can I support the server?",
        value="We currently do not have a webstore or Patreon published, however you can follow or subscribe to our social medias linked below!",
    )
    gamemodeinfo = EmbedField(
        name="What gamemodes can I play?",
        value=f"Our current gamemodes, as of {date}, include Earth and Minigames. "
        "\n \n Earth features a 1:1000 scale map of planet Earth, and includes functionality for things such as towns and nations, a war system, a chest shop in the spawn, and a variety of vehicles including: cars, bikes, planes, helicopters, submarines, and many more!"
        "\n \n Minigames features a variety of minigames, both solo and multiplayer, that you can play! These games include BlockHunt, Dropper, Chess, Zombies, and more to come! \n \n"
    )

    # EmbedFields for networkLinks Embed
    websiteHyperLink = EmbedField(
        name=" ",
        value="Website: [Promethium Network Website](https://www.promethium-network.net/) \n "
        "Webstore: N/A",
    )
    rulesDoc = EmbedField(
        name="Rules Document",
        value="You can find the rules [here](https://docs.google.com/document/d/1EJjC39nwT1pH23ak8VBFCVTYjKpkNm1HA-sMkPsS1FE/edit?usp=sharing)!"
    )
    socialMedias = EmbedField(
        name="Social Medias",
        value="YouTube: [@PromethiumNetwork](https://www.youtube.com/@PromethiumNetwork) "
        "\n TikTok: [@PromethiumNetwork](https://www.tiktok.com/@promethiumnetwork)"
        "\n Patreon: N/A"
    )

    # EmbedFields for LastUpdatedMessage Embed
    lastUpdate = EmbedField(
        name=" ",
        value=f"Message Last Updated on: {date}",
    )

    # Embeds to be sent in ctx.send()
    networkInfo = Embed(title="Promethium Network Info",
                        color="#991aed", fields=[aboutServer, joinInfo, gamemodeinfo, howSupport])
    networkLinks = Embed(title="Promethium Network Links",
                         color="#991aed", fields=[websiteHyperLink, rulesDoc, socialMedias])
    LastUpdatedMessage = Embed(
        title="Last Updated", color="#991aed", fields=[lastUpdate])

    # Set image of logoEmbed to Promethium Network logo
    await ctx.send(embeds=[networkInfo, networkLinks, LastUpdatedMessage])


@slash_command(
    name="roles",
    description="Post the roles embed",
)
async def roles(ctx: SlashContext):
    # EmbedField to be sent in embed in ctx.send()
    rolesEmbedField = EmbedField(
        name="Reaction Roles",
        value="React to receive one of the following roles: \n \n :bar_chart: Polls \n :scroll: Changelog \n :crossed_swords: Events \n :eyes: Sneak Peeks \n :tada: Giveaways"
    )
    await ctx.send(embeds=Embed(title=" ", color="#991aed", fields=[rolesEmbedField]))


@slash_command(
    name="serverstatus",
    description="Posts the server statuses in an embed"
)
@slash_option(
    name='server_opt',
    description='Server Option',
    required=True,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="Earth", value="5699e48e"),
        SlashCommandChoice(name="Minigames", value="6071e3b1"),
        SlashCommandChoice(name="Proxy", value="668c3823")
    ]
)
async def serverstatus(ctx: SlashContext, server_opt: str):
    headers = {
        'Authorization': f'Bearer {os.environ.get("PANEL_TOKEN")}',
        'Content-Type': 'application/json',
        'Accept': 'Application/vnd.pterodactyl.v1+json'
    }

    getserver = requests.get(
        f'https://panel.promethium-network.net/api/client/servers/{server_opt}/resources', headers=headers)

    serverstatus = getserver.json()["attributes"]["current_state"]

    serverstatusemoji = ""
    servername = ''
    color = ""
    servertype = ""

    if serverstatus == 'running':
        serverstatusemoji = ":green_circle:"
        color = "#257016"
    elif serverstatus == 'starting':
        serverstatusemoji = ":yellow_circle:"
        color = "#c9de12"
    else:
        serverstatusemoji = ":red_circle:"
        color = "#de2312"

    if server_opt == '668c3823':
        servername = 'Proxy'
        servertype = "proxy"
    elif server_opt == '5699e48e':
        servername = 'Earth'
        servertype = "server"
    elif server_opt == '6071e3b1':
        servername = 'Minigames'
        servertype = "server"
    else:
        servername = 'INVALID'

    # print(serverstatus)
    serverField = EmbedField(
        name=f"{serverstatusemoji} | The {servertype} is currently {serverstatus}", value=" ")
    serverEmbed = Embed(
        title=f"{servername} Status", fields=[serverField], color=color)
    await ctx.send(embeds=serverEmbed)

# Load extensions
for ext in extensions:
    bot.load_extension(ext)
    print(f"{ext} Loaded!")

# Start PromethiumBot
bot.start(os.environ.get("TOKEN"))
