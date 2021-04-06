import json
import discord
from discord.ext import commands

class accountActions():
    async def accountCreate(name, score, points, context):   
        with open('accounts.json') as fileName:
            file = json.load(fileName)
            new_account = { name : {'score' : int(score), 'points' : int(points)}}
            file.update(new_account)
            with open('accounts.json', 'w') as fileEdit:
                json.dump(file, fileEdit, indent=4)
                await context.send("Your account was created")

    async def accountCheck(name, context):
            with open('accounts.json') as mainFile:
                file = json.load(mainFile)
                if str(name) in file:
                    await context.send("Your account already exists")
                else:
                    await accountCreate(name, 0, 0, context)



    async def deleteAccount(name, context):
        with open('accounts.json') as f:
            json_file = json.load(f)
            json_file.pop(name)
            with open('accounts.json', 'w') as file:
                json.dump(json_file, file, indent=4)
                await context.send("Aww.. We are sad to see you going.. ")