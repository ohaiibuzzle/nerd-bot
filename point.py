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
    
    async def pointAdd(point, name, ctx):
        with open('accounts.json') as file:
            json_data = json.load(file)
            if name in json_data:
                person_folder = json_data[name]
                score = json_data[name]["points"]
                score += point
                person_folder.update({'points' : score})
                with open('accounts.json', 'w') as fileEdit:
                    json.dump(json_data, fileEdit, indent=4)
                    print("Points were added")
            else:
                await ctx.send("You don't have an account.. Create one first. Use `!!createac`")

        