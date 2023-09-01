# Name: skillstop.py
# Parent File: main.py
# Date: 8-30-23
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
playerStatsDict = {}
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
            statement = f"SELECT ID, {skill} FROM s9_skills.SkillData"
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
        match skill:
            case "AGILITY_LEVEL":
                skillName = ":leg: Agility"
            case "ENDURANCE_LEVEL":
                skillName = ":yellow_heart: Endurance"
            case "ENCHANTING_LEVEL":
                skillName = ":magic_wand: Enchanting"
            case "EXCAVATION_LEVEL":
                skillName = ":hammer_pick: Excavation"
            case "FARMING_LEVEL":
                skillName = ":tractor: Farming"
            case "FISHING_LEVEL":
                skillName = ":fishing_pole_and_fish: Fishing"
            case "FORAGING_LEVEL":
                skillName = ":axe: Foraging"
            case "MINING_LEVEL":
                skillName = ":pick: Mining"
            case "FORGING_LEVEL":
                skillName = ":hammer: Forging"
        results = get_results()
        for item in results:
            playerStatsDict.update({f"{api.get_username(uuid=item[0])}":
                                    item[1]})
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
