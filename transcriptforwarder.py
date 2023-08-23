# Name: transcriptForwarder.py
# Parent File: main.py
# Date: 7-20-23
# Author: Shradinx
# -------------------------------

# Import modules
import interactions


class TranscriptForwarder(interactions.Extension):

    # Define function to initialize client
    def __init__(self, client: interactions.Client):
        self.client = client

    @interactions.listen()
    async def on_message_create(self, event: interactions.Message):
        # Check if the message is from Ticket Tool and in #ticket-transcripts
        if event.message.author.id == 557628352828014614 and event.message.channel == 1125955352198926458:
            # Fetch channels from public and staff discord
            transcriptBackupChannel = await self.client.fetch_channel(1126144654950269001)

            # Send the attachments and embeds to #transcript-backups
            await transcriptBackupChannel.send(f"{event.message.attachments[0].url}", embeds=event.message.embeds[0])


def setup(client):
    TranscriptForwarder(client)
