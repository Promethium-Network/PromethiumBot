import interactions
import requests
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()


class ServerStatus(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client = client
