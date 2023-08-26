# Name: skillstop.py
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
playerStatsDict = {}
levelIndex = 0
skillRowIndex = 0
skillName = ""


class SkillStats(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client = client

    @interactions.slash_command(
        name="skillstop",
        description="View the top 10 players for a skill"
    )
    @interactions.slash_option(
        name="skill",
        description="Skill level",
        required=True,
        opt_type=interactions.OptionType.STRING,
        choices=skillNameList
    )
    async def skillstop(self, ctx: interactions.SlashContext, skill: str):
        def get_results():
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
            db.disconnect()
            return results
        
        await ctx.defer()
        skillLevelList.clear()

        match skill:
            case "AGILITY_LEVEL":
                levelIndex = 1
                skillName = ":leg: Agility"
            case "ENDURANCE_LEVEL":
                levelIndex = 2
                skillName = ":yellow_heart: Endurance"
            case "ENCHANTING_LEVEL":
                levelIndex = 3
                skillName = ":magic_wand: Enchanting"
            case "EXCAVATION_LEVEL":
                levelIndex = 4
                skillName = ":hammer_pick: Excavation"
            case "FARMING_LEVEL":
                levelIndex = 5
                skillName = ":tractor: Farming"
            case "FISHING_LEVEL":
                levelIndex = 6
                skillName = ":fishing_pole_and_fish: Fishing"
            case "FORAGING_LEVEL":
                levelIndex = 7
                skillName = ":axe: Foraging"
            case "MINING_LEVEL":
                levelIndex = 8
                skillName = ":pick: Mining"
            case "FORGING_LEVEL":
                levelIndex = 9
                skillName = ":hammer: Forging"

        results = get_results()

        for item in results:
            uuid = item[0]
            minecraftUser = api.get_username(uuid=uuid)
            playerStatsDict.update({f"{minecraftUser}": 
                item[levelIndex]})

        skillLevelList.sort(reverse=True)
        sorted_playerStatsDict = sorted(
            playerStatsDict.items(), key=lambda x: int(x[1]), reverse=True)
        sorted_playerStatsDict = sorted_playerStatsDict[:10]
        statListEmbedFields = []
        place = 1
        for item in sorted_playerStatsDict:
            if item[0] == None:
                statListEmbedFields.append(interactions.EmbedField(
                    name=f"#{place}. N/A | Level: N/A", value=" "))
            else:
                statListEmbedFields.append(interactions.EmbedField(
                    name=f"#{place}. {item[0]} | Level: {item[1]}", value=" "))
            place += 1
        await ctx.send(embed=[interactions.Embed(title=f"{skillName} Leaderboard", fields=statListEmbedFields, color="#991aed")])
        sorted_playerStatsDict.clear()
        playerStatsDict.clear()