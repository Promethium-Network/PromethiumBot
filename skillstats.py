import interactions
import mysql.connector as db_connector
import os
from mojang import API

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
levelIndex = 0
skillRowIndex = 0
skillName = ""

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


class SkillStats(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client = client

    @interactions.slash_command(
        name="skillstats",
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
    async def skillstats(self, ctx: interactions.SlashContext, user: str, skill: str):
        await ctx.defer()

        skillLevelList.clear()
        skillXPList.clear()
        if skill == "AGILITY_LEVEL":
            levelIndex = 1
            xpIndex = 10
            skillName = "Agility"
        elif skill == "ENDURANCE_LEVEL":
            levelIndex = 2
            xpIndex = 11
            skillName = "Endurance"
        elif skill == "ENCHANTING_LEVEL":
            levelIndex = 3
            xpIndex = 12
            skillName = "Enchanting"
        elif skill == "EXCAVATION_LEVEL":
            levelIndex = 4
            xpIndex = 13
            skillName = "Excavation"
        elif skill == "FARMING_LEVEL":
            levelIndex = 5
            xpIndex = 14
            skillName = "Farming"
        elif skill == "FISHING_LEVEL":
            levelIndex = 6
            xpIndex = 15
            skillName = "Fishing"
        elif skill == "FORAGING_LEVEL":
            levelIndex = 7
            xpIndex = 16
            skillName = "Foraging"
        elif skill == "MINING_LEVEL":
            levelIndex = 8
            xpIndex = 17
            skillName = "Mining"
        elif skill == "FORGING_LEVEL":
            levelIndex = 9
            xpIndex = 18
            skillName = "Forging"

        for i in range(len(results)):
            uuid = results[i][0]
            skillLevelList.append(results[i][levelIndex])
            skillXPList.append(results[i][xpIndex])
            if api.get_username(uuid) == user:
                skillLevelIndex = i
                skillXPIndex = i
                break
        nameField = interactions.EmbedField(name="Player Name", value=f"{user}")
        levelField = interactions.EmbedField(name="Skill Level", value=f"{skillLevelList[skillLevelIndex]}")
        xpField = interactions.EmbedField(name="Skill XP", value=f"{skillXPList[skillXPIndex]}")
        skillEmbed = interactions.Embed(title=f"{skillName} Skill Info", description=" ", fields=[nameField, levelField, xpField], color="#991aed")
        await ctx.send(embed=[skillEmbed])