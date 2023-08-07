# Name: serverStatusEmbeds.py
# Parent File: main.py
# Date: 8-6-23
# Author: Shradinx
# -------------------------------

# import modules
import interactions
from interactions import Client, Intents, listen, slash_command, SlashContext, Embed, EmbedField, EmbedFooter, EmbedAuthor, EmbedAttachment, slash_option, OptionType, SlashCommandChoice
import os
import requests
from pydantic import BaseModel

# define variables
serverstatusemoji = ""
servername = ''
color = ""
servertype = "server"
serverList = [
    "668c3823",
    "b6b6b508",
    "6071e3b1",
    "5699e48e",
]
fieldList = []

# define function to get info for server, proxy, or both


def get_server_info(self, server):
    global serverstatusemoji
    global servername
    global color
    global servertype
    global fieldList
    global serverstatus
    headers = {
        'Authorization': f'Bearer {os.environ.get("PANEL_TOKEN")}',
        'Content-Type': 'application/json',
        'Accept': 'Application/vnd.pterodactyl.v1+json'
    }

    getserver = requests.get(
        f'https://panel.promethium-network.net/api/client/servers/{server}/resources', headers=headers)
    serverstatus = getserver.json()["attributes"]["current_state"]

    if serverstatus == 'running':
        serverstatusemoji = ":green_circle:"
        color = "#257016"
    elif serverstatus == 'starting':
        serverstatusemoji = ":yellow_circle:"
        color = "#c9de12"
    else:
        serverstatusemoji = ":red_circle:"
        color = "#de2312"

    if server == '668c3823':
        servername = 'Proxy'
        servertype = "proxy"
    elif server == '5699e48e':
        servername = 'Earth'
        servertype = "server"
    elif server == '6071e3b1':
        servername = 'Minigames'
        servertype = "server"
    elif server == "b6b6b508":
        servername = "Lobby"
        servertype = "server"
    elif server == "ALL":
        servername = "All Servers and Proxy"
    else:
        servername = 'INVALID'


# define class for embed posting
class ServerStatusEmbeds(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client = client

    @slash_command(
        name="serverstatus",
        description="Posts a server or the proxy's status in an embed"
    )
    @slash_option(
        name='server',
        description='Server/Proxy',
        required=True,
        opt_type=OptionType.STRING,
        choices=[
            SlashCommandChoice(name="Earth", value="5699e48e"),
            SlashCommandChoice(name="Minigames", value="6071e3b1"),
            SlashCommandChoice(name="Lobby-1", value="b6b6b508"),
            SlashCommandChoice(name="Proxy", value="668c3823"),
            SlashCommandChoice(name="All", value="ALL"),
        ]
    )
    async def serverstatus(self, ctx: SlashContext, server: str):
        if server == "ALL":
            await ctx.defer()
            for server in serverList:
                get_server_info(self, server)
                fieldList.append(EmbedField(
                    name=f"{serverstatusemoji} {servername} Status", value=f"The {servertype} is currently {serverstatus}"))
            serverEmbed = Embed(
                title=f"Proxy and Servers Status", fields=fieldList, color="#991aed")
            await ctx.send(embeds=serverEmbed)
        else:
            get_server_info(self, server)
            # print(serverstatus)
            serverField = EmbedField(
                name=f"The {servertype} is currently {serverstatus}", value=" ")
            serverEmbed = Embed(
                title=f"{serverstatusemoji} {servername} Status", fields=[serverField], color=color)
            await ctx.send(embeds=serverEmbed)
