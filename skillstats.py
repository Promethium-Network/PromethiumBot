# Name: skillstats.py
# Parent File: main.py
# Date: 8-18-23
# Author: Shradinx
# -------------------------------

import interactions
import mysql.connector as db_connector
import os
from mojang import API

# moblang api
api = API()

hostname = os.environ.get("DB_HOST")
username = os.environ.get("DB_SKILLS_USER")
password = os.environ.get("DB_SKILLS_PASS")
dbName = os.environ.get("DB_SKILLS_NAME")

statement = "SELECT ID, AGILITY_LEVEL, ENDURANCE_LEVEL, ENCHANTING_LEVEL, EXCAVATION_LEVEL, FARMING_LEVEL, FISHING_LEVEL, FORAGING_LEVEL, MINING_LEVEL, FORGING_LEVEL, AGILITY_XP, ENDURANCE_XP, ENCHANTING_XP, EXCAVATION_XP, FARMING_XP, FISHING_XP, FORAGING_XP, MINING_XP, FORGING_XP FROM s9_skills.SkillData"
playerList = []

skillNameList = [
    interactions.SlashCommandChoice(name="Agility", value="AGILITY_LEVEL"),
    interactions.SlashCommandChoice(name="Endurance", value="ENDURANCE_LEVEL"),
    interactions.SlashCommandChoice(
        name="Enchanting", value="ENCHANTING_LEVEL"),
    interactions.SlashCommandChoice(
        name="Excavation", value="EXCAVATION_LEVEL"),
    interactions.SlashCommandChoice(name="Farming", value="FARMING_LEVEL"),
    interactions.SlashCommandChoice(name="Fishing", value="FISHING_LEVEL"),
    interactions.SlashCommandChoice(name="Foraging", value="FORAGING_LEVEL"),
    interactions.SlashCommandChoice(name="Mining", value="MINING_LEVEL"),
    interactions.SlashCommandChoice(name="Forging", value="FORGING_LEVEL"),
]
skillLevelList = []
skillXPList = []
playerStatsDict = {}
levelIndex = 0
xpIndex = 0
skillRowIndex = 0
skillName = ""

# connect to skills database
db = db_connector.connect(
    host=hostname,
    user=username,
    password=password,
    database=dbName,
)
# execute statement and fetch the results
cursor = db.cursor()
cursor.execute(statement)
results = cursor.fetchall()
for i in range(len(results)):
    # get the user uuid
    uuid = results[i][0]
    # convert to minecraft username
    minecraftUser = api.get_username(uuid=uuid)
    # add slash command choice to player list with username
    playerList.append(interactions.SlashCommandChoice(
        name=minecraftUser, value=minecraftUser))
db.disconnect()


class SkillStats(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client = client

    @interactions.listen()
    async def on_extension_load(self, extension: interactions.Extension):
        if extension.extension.name == "SkillStats":
            async def getPlayers():
                # connect to skills database
                db = db_connector.connect(
                    host=hostname,
                    user=username,
                    password=password,
                    database=dbName,
                )
                # execute statement and fetch the results
                cursor = db.cursor()
                cursor.execute(statement)
                results = cursor.fetchall()
                for i in range(len(results)):
                    # get the user uuid
                    uuid = results[i][0]
                    # convert to minecraft username
                    minecraftUser = api.get_username(uuid=uuid)
                    # add slash command choice to player list with username
                    playerList.append(interactions.SlashCommandChoice(
                        name=minecraftUser, value=minecraftUser))
                db.disconnect()
                print("Disconnected from Skills Database")

            task = interactions.Task(
                getPlayers, interactions.IntervalTrigger(minutes=5))

    @interactions.slash_command(
        name="skillstats",
        description="just learning python mysql databases thats all :)"
    )
    @interactions.slash_option(
        name="skill",
        description="Skill level",
        required=True,
        opt_type=interactions.OptionType.STRING,
        choices=skillNameList
    )
    async def skillstats(self, ctx: interactions.SlashContext, skill: str):
        playerList.clear()
        skillLevelList.clear()
        skillXPList.clear()

        match skill:
            case "AGILITY_LEVEL":
                levelIndex = 1
                xpIndex = 10
                skillName = ":leg: Agility"
            case "ENDURANCE_LEVEL":
                levelIndex = 2
                xpIndex = 11
                skillName = ":yellow_heart: Endurance"
            case "ENCHANTING_LEVEL":
                levelIndex = 3
                xpIndex = 12
                skillName = ":magic_wand: Enchanting"
            case "EXCAVATION_LEVEL":
                levelIndex = 4
                xpIndex = 13
                skillName = ":hammer_pick: Excavation"
            case "FARMING_LEVEL":
                levelIndex = 5
                xpIndex = 14
                skillName = ":tractor: Farming"
            case "FISHING_LEVEL":
                levelIndex = 6
                xpIndex = 15
                skillName = ":fishing_pole_and_fish: Fishing"
            case "FORAGING_LEVEL":
                levelIndex = 7
                xpIndex = 16
                skillName = ":axe: Foraging"
            case "MINING_LEVEL":
                levelIndex = 8
                xpIndex = 17
                skillName = ":pick: Mining"
            case "FORGING_LEVEL":
                levelIndex = 9
                xpIndex = 18
                skillName = ":hammer: Forging"

        db = db_connector.connect(
            host=hostname,
            user=username,
            password=password,
            database=dbName,
        )
        # execute statement and fetch the results
        cursor = db.cursor()
        cursor.execute(statement)
        results = cursor.fetchall()

        for i in range(25):
            uuid = results[i][0]
            minecraftUser = api.get_username(uuid=uuid)
            playerStatsDict.update({f"{minecraftUser}": (
                f"{results[i][levelIndex]}", f"{results[i][xpIndex]}")})
            
        skillLevelList.sort(reverse=True)
        skillXPList.sort(reverse=True)
        sorted_playerStatsDict = sorted(
            playerStatsDict.items(), key=lambda x: x[1], reverse=True)
        sorted_playerStatsDict = sorted_playerStatsDict[0:10]
        statListEmbedFields = []
        place = 1
        for i in range(len(sorted_playerStatsDict)):
            statListEmbedFields.append(interactions.EmbedField(
                name=f"#{place}: {sorted_playerStatsDict[i][0]}", value=f"Level: {sorted_playerStatsDict[i][1][0]} | XP: {sorted_playerStatsDict[i][1][1][0:6]}"))
            place += 1
        await ctx.send(embed=[interactions.Embed(title=f"{skillName} Leaderboard", fields=statListEmbedFields, color="#991aed")])
        sorted_playerStatsDict.clear()
        playerStatsDict.clear()
        db.disconnect()
