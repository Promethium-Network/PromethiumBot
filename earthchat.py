import interactions
import requests
from pydantic import BaseModel


class EarthChat(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client = client

    class MessageData(BaseModel):
        author: str
        content: str
        avatar: str

    @interactions.listen()
    async def on_message_create(self, event: interactions.Message):
        if event.message.channel == 1133396297613852812:
            message = MessageData()
            print(event.message.author)
            print(event.message.content)
            print(event.message.author.avatar._url)
