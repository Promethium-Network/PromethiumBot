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
skillIndices = {
    "Agility": (1, 10),
    "Endurance": (2, 11),
    "Enchanting": (3, 12),
    "Excavation": (4, 13),
    "Farming": (5, 14),
    "Fishing": (6, 15),
    "Foraging": (7, 16),
    "Mining": (8, 17),
    "Forging": (9, 18),
    "AGILITY_LEVEL": (1, 10),
}

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
        levelIndex, xpIndex = skillIndices[skill]
        skillLevels, skillXP = zip(*[(results[i][levelIndex], results[i][xpIndex]) for i in range(len(results)) if api.get_username(results[i][0]) == user])
        skillLevel, skillXP = skillLevels[0], skillXP[0]

        nameField = interactions.EmbedField(name="Player Name", value=f"{user}")
        levelField = interactions.EmbedField(name="Skill Level", value=f"{skillLevel}")
        xpField = interactions.EmbedField(name="Skill XP", value=f"{skillXP}")
        skillEmbed = interactions.Embed(title=f"{skill} Skill Info", description=" ", fields=[nameField, levelField, xpField], color="#991aed")
        await ctx.send(embed=[skillEmbed])