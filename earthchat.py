import interactions
import requests
from pydantic import BaseModel


class EarthChat(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client = client

    @interactions.listen()
    async def on_message_create(self, event: interactions.Message):
        class MessageData(BaseModel):
            author: str
            content: str
            avatar: str
        if event.message.channel == 1133396297613852812:
            message = MessageData(
                event.message.author,
                event.message.content,
                event.message.avatar._url
            )
            print(message)
            # print(event.message.author)
            # print(event.message.content)
            # print(event.message.author.avatar._url)
