#  Name: transcriptForwarder.py
#  Parent File: PromethiumBot.py
#  Date: 7-19-23
#  Author: Shradinx
# -------------------------------

'''
    TODO:
    - Get bot to copy the .html file and embed and send it to #bot-testing channel
    - Add bot to staff discord, and then get it to send the embed and .html file in the #transcript-backups channel.
    - Automate it so that everytime a ticket is closed and transcript is made, it is copied to staff discord
'''

# Import modules
import interactions


class transcriptForwarder(interactions.Extension):

    # Define function to initialize client
    def __init__(self, client: interactions.Client):
        self.client = client

    # Print confirmation message
    print("Extension Loaded!")

    # Define /forward slash command
    @interactions.slash_command(
        name="forward",
        description="Get the latest message in #ticket-transcripts"
    )
    # Define function for /forward
    async def forward(self, ctx: interactions.SlashContext):
        # Fetch #ticket-transcripts channel from public discord
        channel = await self.client.fetch_channel(1125955352198926458)

        # Get full channel history, then flatten it from async iterator to list
        history = await channel.history().flatten()

        # For every message in the channel's history, if the author is Ticket Tool, print the embed in the message
        for message in history:
            if message.author.id == 557628352828014614:
                print(message.embeds[0])
                break
        await ctx.send('shit')


def setup(client):
    transcriptForwarder(client)
