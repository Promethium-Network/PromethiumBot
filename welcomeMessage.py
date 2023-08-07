# Name: welcomeMessage.py
# Parent File: main.py
# Date: 7-20-23
# Author: Shradinx
# -------------------------------

# Import modules
import interactions
from interactions import Embed, EmbedField


class WelcomeMessage(interactions.Extension):

    # Define function to initialize client
    def __init__(self, client: interactions.Client):
        self.client = client

    # On member join, print embed welcoming user
    @interactions.listen()
    async def on_member_add(self, event):
        if event.member.guild.id == 1125940812182724698:
            channel = await self.client.fetch_channel(1125942122902732830)
            await channel.send(embeds=Embed(title=" ", color="#991aed", fields=[EmbedField(name=" ", value=f"**Welcome to Promethium Network, {event.member.mention}!**")]))
