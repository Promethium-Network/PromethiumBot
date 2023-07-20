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

    '''
    # Define /forward slash command
    @interactions.slash_command(
        name="forward",
        description="Get the latest message in #ticket-transcripts"
    )
    # Define function for /forward
    async def forward(self, ctx: interactions.SlashContext):
        # Fetch channels from public and staff discord
        ticketChannel = await self.client.fetch_channel(1125955352198926458)
        transcriptBackupChannel = await self.client.fetch_channel(1126144654950269001)

        # Get full channel history, then flatten it from async iterator to list
        history = await ticketChannel.history().flatten()

        # For every message in the channel's history, if the author is Ticket Tool, print the embed in the message
        for message in history:
            if message.author.id == 557628352828014614:
                await transcriptBackupChannel.send(f"{message.attachments[0].url}", embeds=message.embeds[0])
                await ctx.send("Transcript copied to Staff Discord!")
                break
    '''

    @interactions.listen()
    async def on_message_create(self, event: interactions.Message):
        if event.message.author.id == 557628352828014614 and event.message.channel == 1125955352198926458:
            # Fetch channels from public and staff discord
            ticketChannel = await self.client.fetch_channel(1125955352198926458)
            transcriptBackupChannel = await self.client.fetch_channel(1126144654950269001)
            botTesting = await self.client.fetch_channel(1130893800357773312)

            await transcriptBackupChannel.send(f"{event.message.attachments[0].url}", embeds=event.message.embeds[0])
            await botTesting.send("Transcript copied to Staff Discord!")


def setup(client):
    transcriptForwarder(client)
