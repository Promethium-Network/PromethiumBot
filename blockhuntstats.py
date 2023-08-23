import interactions
import mysql.connector as db_connector
import os
from mojang import API

api = API()
statList = [
    interactions.SlashCommandChoice(name="Wins", value="wins"),
    interactions.SlashCommandChoice(name="Coins", value="coins"),
    interactions.SlashCommandChoice(name="Games Played", value="games_played"),
    interactions.SlashCommandChoice(name="Hiders Killed", value="hiders_killed"),
    interactions.SlashCommandChoice(name="Seekers Killed", value="seekers_killed"),
]
statement = 'select player_name, wins, coins, games_played, hiders_killed, seekers_killed from s8_blockhunt.HideAndSeek'
hostname = os.environ.get("DB_HOST")
username = os.environ.get("DB_BLOCKHUNT_USER")
password = os.environ.get("DB_BLOCKHUNT_PASS")
dbName = os.environ.get("DB_BLOCKHUNT_NAME")


class blockHuntStats(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client = client

    @interactions.slash_command(
        name="blockhuntstats",
        description="View the top 10 players for a statistic in BlockHunt"
    )
    @interactions.slash_option(
        name="stat",
        description="BlockHunt Statistic",
        required=True,
        opt_type=interactions.OptionType.STRING,
        choices=statList
    )
    async def blockhuntstats(self, ctx: interactions.SlashContext, stat: str):
        await ctx.defer()
        playerList = []
        statValues = []
        statEmbedFields = []
        index = 0
        statName = ""
        statDict = {}

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
            match stat:
                case "wins":
                    statValues.append(int(results[i][1]))
                    statName = "Wins"
                case "coins":
                    statValues.append(int(results[i][2]))
                    statName = "Coins"
                case "games_played":
                    statValues.append(int(results[i][3]))
                    statName = "Games Played"
                case "hiders_killed":
                    statValues.append(int(results[i][4]))
                    statName = "Hiders Killed"
                case "seekers_killed":
                    statValues.append(int(results[i][5]))
                    statName = "Games Played"
            playerList.append(results[i][0])
            statDict.update({f"{playerList[i]}": f"{statValues[i]}"})

        statValues = statValues[:10]
        sorted_statDict = sorted(
            statDict.items(), key=lambda x: int(x[1]), reverse=True)
        sorted_statDict = sorted_statDict[:10]
        place = 1
        for i in range(10):
            if i >= len(sorted_statDict):
                statEmbedFields.append(interactions.EmbedField(name=f"#{place}. N/A", value=" "))
            else:
                statEmbedFields.append(interactions.EmbedField(name=f"#{place}. {sorted_statDict[i][0]} | {sorted_statDict[i][1]}", value=" "))
            place += 1
        blockHuntStatEmbed = interactions.Embed(title=f"<:grass_block:1143716614680883362> BlockHunt {statName} Leaderboard <:diamond_sword:1143716612243980298>", description=" ", color="#991aed", fields=statEmbedFields)
        await ctx.send(embeds=blockHuntStatEmbed)
        blockhunt.disconnect()
