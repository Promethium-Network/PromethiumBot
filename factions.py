import interactions
import requests
import os
import pydactyl
import yaml

api = pydactyl.PterodactylClient(url='https://panel.promethium-network.net/', api_key=os.environ.get("PANEL_TOKEN"), debug=False)
userList = [
        interactions.SlashCommandChoice(name="balls", value="balls"),
        interactions.SlashCommandChoice(name="balls2", value="balls2"),
    ]

class Factions(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client = client
    

    
    @interactions.slash_command(
        name="faction",
        description="Display a user's faction",
    )
    @interactions.slash_option(
        name="user",
        description="The user to get faction info for",
        required=True,
        opt_type=interactions.OptionType.STRING,
        choices=userList
    )
    async def faction(self, ctx: interactions.SlashContext, user: str):
        file = api.client.servers.files.get_file_contents("5699e48e", "/plugins/SevenFactions/factions.yml")
        ball = yaml.safe_load(file.text)
        print(ball["factions"]["06472bd1-46b4-4b81-9d75-6e83995d4bee"]["name"])
        await ctx.send("balls")