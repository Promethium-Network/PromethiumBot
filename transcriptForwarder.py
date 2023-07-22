# Name: transcriptForwarder.py
# Parent File: PromethiumBot.py
# Date: 7-20-23
# Author: Shradinx
# -------------------------------

# Import modules
import interactions


class transcriptForwarder(interactions.Extension):

    # Define function to initialize client
    def __init__(self, client: interactions.Client):
        self.client = client

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
        # Check if the message is from Ticket Tool and in #ticket-transcripts
        if event.message.author.id == 557628352828014614 and event.message.channel == 1125955352198926458:
            # Fetch channels from public and staff discord
            ticketChannel = await self.client.fetch_channel(1125955352198926458)
            transcriptBackupChannel = await self.client.fetch_channel(1126144654950269001)
            botTesting = await self.client.fetch_channel(1130893800357773312)

            # Send the attachments and embeds to #transcript-backups
            await transcriptBackupChannel.send(f"{event.message.attachments[0].url}", embeds=event.message.embeds[0])


def setup(client):
    transcriptForwarder(client)
