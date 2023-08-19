import interactions
import mysql.connector as db_connector
import os
from mojang import API

api = API()

hostname = os.environ.get("DB_HOST")
username = os.environ.get("DB_BLOCKHUNT_USER")
password = os.environ.get("DB_BLOCKHUNT_PASS")
dbName = os.environ.get("DB_BLOCKHUNT_NAME")

statement = 'select player_name, wins, coins, games_played from s8_blockhunt.HideAndSeek'
playerList = []
wins = []
coins = []
games_played = []
index = 0

blockhunt = db_connector.connect(
    host=hostname,
    user=username,
    password=password,
    database=dbName,
)

cursor = blockhunt.cursor()
cursor.execute(statement)
results = cursor.fetchall()
for i in range(len(results)):
    minecraftIGN = results[i][0]
    # add slash command choice to player list with username
    playerList.append(interactions.SlashCommandChoice(
        name=minecraftIGN, value=minecraftIGN))


class blockHuntStats(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client = client

    @interactions.slash_command(
        name="blockhuntstats",
        description="View a player's stats for BlockHunt"
    )
    @interactions.slash_option(
        name="user",
        description="Minecraft Player Name",
        required=True,
        opt_type=interactions.OptionType.STRING,
        choices=playerList
    )
    async def blockhuntstats(self, ctx: interactions.SlashContext, user: str):
        playerList.clear()
        wins.clear()
        coins.clear()
        games_played.clear()

        for i in range(len(results)):
            wins.append(results[i][1])
            coins.append(results[i][2])
            games_played.append(results[i][3])
            if results[i][0] == user:
                index = i
                break
        winsField = interactions.EmbedField(name="Wins", value=f"{wins[index]}")
        coinsField = interactions.EmbedField(name="Coins", value=f"{coins[index]}")
        gamesPlayedField = interactions.EmbedField(name="Games Played", value=f"{games_played[index]}")
        blockHuntStatEmbed = interactions.Embed(title=f"{user}'s BlockHunt Stats", description=" ", color="#991aed", fields=[winsField, coinsField, gamesPlayedField])
        await ctx.send(embeds=blockHuntStatEmbed)
        
blockhunt.close()
