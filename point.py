import json
import discord
from discord.ext import commands

class points:
    async def pointsCount(name, context):
        with open('accounts.json') as json_file:
            data = json.load(json_file)
            
            if name in data:
                score =  data[name]['points']
                pointsEmbed = discord.Embed(title = f"{name}", description = f"Your score is: `{score}`")
                await context.send(embed = pointsEmbed)
            else:
                await context.send("Oops seems like you don't have an account")
        