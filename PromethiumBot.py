#  Name: PromethiumBot.py
#  Date: 7-19-23
#  Author: Shradinx
# --------------------------------------

'''
	TODO: 
	- Finish server info embed
		= Add voting hyperlinks
        = Add website hyperlink (when gus is able to make site public)
        = Replace logo embed with gamemode info embed
    - Finish transcript forwarder
		= Refer to transcriptForwarder.py to do list
'''

# Import modules
import interactions
from interactions import Client, Intents, listen, slash_command, SlashContext, Embed, EmbedField, EmbedFooter, EmbedAuthor, EmbedAttachment
import datetime
from dotenv import load_dotenv
import os
load_dotenv()

# Define activity status
activity = interactions.Activity.create(
    name="play.promethium-network.net",
    type=interactions.ActivityType.PLAYING,
)

# Define bot client, along with intents and display activity status
bot = Client(intents=Intents.DEFAULT |
             Intents.MESSAGE_CONTENT, activity=activity)


@listen()
async def on_ready():
    print("PromethiumBot Online!")


@slash_command(
    name="serverinfo",
    description="Post the server info embed",
)
async def serverinfo(ctx: SlashContext):
    date = str(datetime.datetime.now().strftime("%x"))
    logo = interactions.File("promethium-transparent-resize.png")

    # EmbedFields for networkinfo Embed
    aboutServer = EmbedField(
        name="About Promethium Network",
        value="Promethium Network is a Minecraft server managed and owned by Shradinx and Gusbunce. "
        "\n \nIt was started in early July 2023 when Geographica, a previous Minecraft server, was announced to be shutting down."
        "\n  \nBelow, you can find other information about the server, such as links to our rules document, our social medias, and our Patreon."
    )
    joinInfo = EmbedField(
        name="\n How to join Promethium Network?",
        value="You can join our in-game Minecraft server by connecting to play.promethium-network.net on 1.19.4 and above!"
    )
    howSupport = EmbedField(
        name="How can I support the server?",
        value="You can support our server by joining our Patreon, following our social medias, donating to our webstore, and voting for our server!",
    )

    # EmbedFields for networkLinks Embed
    websiteHyperLink = EmbedField(
        name=" ",
        value="[Promethium Network Website](https://www.promethium-network.net)",
    )
    rulesDoc = EmbedField(
        name="Rules Document",
        value="You can find the rules [here](https://docs.google.com/document/d/1EJjC39nwT1pH23ak8VBFCVTYjKpkNm1HA-sMkPsS1FE/edit?usp=sharing)!"
    )
    socialMedias = EmbedField(
        name="Social Medias",
        value="YouTube: [@PromethiumNetwork](https://www.youtube.com/@PromethiumNetwork) "
        "\n Twitter: [@PromethiumMC1](https://twitter.com/PromethiumMC1)"
        "\n Patreon: [PromethiumMinecraft](https://patreon.com/PromethiumMinecraft)"
    )

    # EmbedFields for LastUpdatedMessage Embed
    lastUpdate = EmbedField(
        name=" ",
        value=f"Message Last Updated on: {date}",
    )

    # Embeds to be sent in ctx.send()
    networkInfo = Embed(title="Promethium Network Info",
                        color="#991aed", fields=[aboutServer, joinInfo, howSupport])
    networkLinks = Embed(title="Promethium Network Links",
                         color="#991aed", fields=[websiteHyperLink, rulesDoc, socialMedias])
    LastUpdatedMessage = Embed(
        title="Last Updated", color="#991aed", fields=[lastUpdate])
    logoEmbed = Embed(title=" ", color="#991aed", fields=[])

    # Set image of logoEmbed to Promethium Network logo
    logoEmbed.set_image(url="attachment://promethium-transparent-resize.png")
    await ctx.send(embeds=[networkInfo, networkLinks, logoEmbed, LastUpdatedMessage], file=logo)


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

# Load transcriptForwarder extension
bot.load_extension("transcriptForwarder")

# Start PromethiumBot
bot.start(os.environ.get("TOKEN"))
