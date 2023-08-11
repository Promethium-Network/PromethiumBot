# Name: playerstats.py
# Parent File: main.py
# Date: 8-10-23
# Author: gusbuncedev
# -------------------------------

import interactions
from interactions import listen, slash_command, SlashContext, Embed, EmbedField, EmbedFooter, EmbedAuthor, EmbedAttachment, slash_option, OptionType, SlashCommandChoice
import os
from pydantic import BaseModel
import mysql.connector as database
from datetime import datetime as dt

username = os.environ.get("DB_USER")
password = os.environ.get("DB_PASS")
host = os.environ.get("DB_HOST")
db = os.environ.get("DB_NAME")

connection = database.connect(
    user=username,
    password=password,
    host=host,
    database=db
)

cursor = connection.cursor()


class PlayerStats(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client = client

    player_list = []
    try:
        statement = "SELECT name FROM s6_plan.plan_users"
        cursor.execute(statement)
        for (name) in cursor:
            player_list.append(SlashCommandChoice(name=name[0], value=name[0]))
    except database.Error as e:
        print(
            f"Sorry an error occured while fetching data please contact gusbuncedev with the following error: {e}")

    @slash_command(
        name='playerstats',
        description='Dev: Returns all players that have ever played on the server'
    )
    @slash_option(
        name='player',
        description='Player Name',
        required=True,
        opt_type=OptionType.STRING,
        choices=player_list
    )
    async def playerstats(self, ctx: SlashContext, player: str):
        try:
            statement = "SELECT name, registered FROM s6_plan.plan_users WHERE name=%s"
            data = (player,)
            cursor.execute(statement, data)
            for (name, registered) in cursor:
                statusEmbedField = EmbedField(
                    name=f"{name} has been playing since <t:{int(registered/1000.0)}:R>!", value=" ")
                await ctx.send(embeds=[Embed(title=" ", fields=[statusEmbedField], color="#991aed")])
        except database.Error as e:
            db_errorField = EmbedField(
                name=f"Sorry an error occured while fetching data please contact gusbuncedev with the following error: {e}", value="")
            await ctx.send(embeds=[Embed(title=" ", fields=[db_errorField], color="#000000")])
