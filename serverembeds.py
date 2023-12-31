# Name: serverEmbeds.py
# Parent File: main.py
# Date: 8-6-23
# Author: Shradinx
# -------------------------------

# import modules
import interactions
from interactions import EmbedField, Embed
from datetime import datetime

'''
	TODO:
	- Finish server info embed
		= Add voting hyperlinks
'''

'''
Copy-Paste List:




'''

# define class for server embeds


class ServerEmbeds(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client = client

    # define command + function to post the server info embed
    @interactions.slash_command(
        name="serverinfo",
        description="Post the server info embed",
    )
    async def server_info(self, ctx: interactions.SlashContext):
        date = datetime.now().strftime("%x")

        # EmbedFields for networkinfo Embed
        aboutServer = EmbedField(
            name="About Promethium Network",
            value="Promethium Network is a Minecraft server network managed and owned by Shradinx and gusbunce. "
            "\n \nIt was started in early July 2023 when Geographica, a previous Minecraft server, was announced to be shutting down."
            "\n  \nBelow, you can find other information about the server, such as links to our rules document and our social medias. \n \n"
        )
        joinInfo = EmbedField(
            name="\n How to join Promethium Network?",
            value="Starting August 19th, you can join our in-game Minecraft server by connecting to **play.promethium-network.net** on 1.19.4 and above!"
            "\n \n It is recommended that you have **Resource Packs: Enabled** set prior to joining the server!"
        )
        howSupport = EmbedField(
            name="How can I support the server?",
            value="You can support our server by joining our Patreon, following our social medias, donating to our webstore, and voting for our server!",
        )
        gamemodeinfo = EmbedField(
            name="What gamemodes can I play?",
            value=f"Our current gamemodes, as of {date}, include Earth and Minigames. "
            "\n \n Earth features a 1:750 scale map of planet Earth, and includes functionality for things such as factions/nations, a chest and GUI shop, Slimefun, a dynamic map that updates every second, and a variety of vehicles including: cars, bikes, planes, helicopters, submarines, and many more!"
            "\n \n Minigames features a variety of minigames, both solo and multiplayer, that you can play! These games include BlockHunt, Dropper, Chess, Zombies, and more to come!"
            "\n \n All of our servers also support Vivecraft, a VR version of Minecraft, and SimpleVoiceChat, a proximity voice chat mod!"
        )

        # EmbedFields for networkLinks Embed
        websiteHyperLink = EmbedField(
            name=" ",
            value="Website: [Promethium Network Website](https://promethium-network.net/) \n "
            "Webstore: [Promethium Network Store](https://store.promethium-network.net) \n Discord Invite: https://discord.gg/jbFwC4eSaT \n"
            "Dynmap: [Promethium Network Dynmap](https://map.promethium-network.net)",
        )
        rulesDoc = EmbedField(
            name="Rules Document",
            value="You can find the rules [here](https://docs.google.com/document/d/1EJjC39nwT1pH23ak8VBFCVTYjKpkNm1HA-sMkPsS1FE/edit?usp=sharing)!"
        )
        socialMedias = EmbedField(
            name="Social Medias",
            value="YouTube: [@PromethiumNetwork](https://www.youtube.com/@PromethiumNetwork) "
            "\n TikTok: [@PromethiumNetwork](https://www.tiktok.com/@promethiumnetwork)"
            "\n Patreon: [PromethiumMinecraft](https://patreon.com/PromethiumMinecraft)"
        )
        voteSites = EmbedField(
            name="Voting Links",
            value="[Minecraft Server List](https://minecraft-server-list.com/server/499493/) "
            "\n [MinecraftServers.org](https://minecraftservers.org/server/655193)"
        )
        developmentLinks = EmbedField(
            name="Development Links",
            value="GitHub: [Promethium-Network](https://github.com/Promethium-Network)"
        )

        # EmbedFields for LastUpdatedMessage Embed
        lastUpdate = EmbedField(
            name=" ",
            value=f"Message Last Updated on: {date}",
        )

        # Embeds to be sent in ctx.send()
        networkInfo = Embed(title="Promethium Network Info",
                            color="#991aed", fields=[aboutServer, joinInfo, gamemodeinfo, howSupport])
        networkLinks = Embed(title="Promethium Network Links", description="**IP: play.promethium-network.net (1.19.4+)**",
                             color="#991aed", fields=[websiteHyperLink, rulesDoc, socialMedias, voteSites, developmentLinks])
        LastUpdatedMessage = Embed(
            title="Last Updated", color="#991aed", fields=[lastUpdate])

        # Set image of logoEmbed to Promethium Network logo
        await ctx.send(embeds=[networkInfo, networkLinks, LastUpdatedMessage])

    # define command + function to post the roles embed
    @interactions.slash_command(
        name="roles",
        description="Post the roles embed",
    )
    async def roles(self, ctx: interactions.SlashContext):
        # EmbedField to be sent in embed in ctx.send()
        rolesEmbedField = EmbedField(
            name="Reaction Roles",
            value="React to receive one of the following roles: \n \n :bar_chart: Polls \n :scroll: Changelog \n :crossed_swords: Events \n :eyes: Sneak Peeks \n :tada: Giveaways"
        )
        await ctx.send(embeds=Embed(title=" ", color="#991aed", fields=[rolesEmbedField]))
