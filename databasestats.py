import interactions
import mysql.connector as db_connector
import os
import requests
from mojang import API

api = API()

hostname = os.environ.get("DB_HOST")
username = os.environ.get("DB_SKILLS_USER")
password = os.environ.get("DB_SKILLS_PASS")
dbName = os.environ.get("DB_SKILLS_NAME")
statement = "SELECT ID, AGILITY_LEVEL, ENDURANCE_LEVEL, ENCHANTING_LEVEL, EXCAVATION_LEVEL, FARMING_LEVEL, FISHING_LEVEL, FORAGING_LEVEL, MINING_LEVEL, FORGING_LEVEL FROM s9_skills.SkillData"
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
index = 0

db = db_connector.connect(
    host=hostname,
    user=username,
    password=password,
    database=dbName,
)
cursor = db.cursor()
cursor.execute(statement)
results = cursor.fetchall()
for i in range(len(results)):
    uuid = results[i][0]
    minecraftUser = api.get_username(uuid=uuid)
    playerList.append(interactions.SlashCommandChoice(
        name=minecraftUser, value=minecraftUser))


class DatabaseTests(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client = client

    @interactions.slash_command(
        name="database",
        description="just learning python mysql databases thats all :)"
    )
    @interactions.slash_option(
        name="user",
        description="Minecraft Player Name",
        required=True,
        opt_type=interactions.OptionType.STRING,
        choices=playerList
    )
    @interactions.slash_option(
        name="skill",
        description="Skill level",
        required=True,
        opt_type=interactions.OptionType.STRING,
        choices=skillNameList
    )
    async def database(self, ctx: interactions.SlashContext, user: str, skill: str):
        await ctx.defer()
        if skill == "ENDURANCE_LEVEL":
            for i in range(len(results)):
                uuid = results[i][0]
                skillLevelList.append(results[i][2])
                if api.get_username(uuid) == user:
                    index = i
                    break
            await ctx.send(f"{user} | {skillLevelList[index]}")
