import json
import discord
from discord.embeds import Embed
from discord.ext import commands
from .embeds import Embeds
import random

class accountActions:
    @staticmethod
    def accountBoolean(name):
        with open('./data/accounts.json') as mainFile:
            file = json.load(mainFile)
            if str(name) in file:
                return True
            else:
                return False
        
    async def accountCheck(self, name, context):
        with open('./data/accounts.json') as mainFile:
            file = json.load(mainFile)
            if accountActions.accountBoolean(name) == True:
                await context.send("Your account already exists")
            else:
                await self.accountCreate(name, 0, 0, context)

    async def accountCreate(self, name, score, points, context):   
        with open('./data/accounts.json') as fileName:
            file = json.load(fileName)
            new_account = { name : {'score' : int(score), 'points' : int(points), 'powers' : []}}
            file.update(new_account)
            with open('./data/accounts.json', 'w') as fileEdit:
                json.dump(file, fileEdit, indent=4)
                await context.send("Your account was created")

    @staticmethod
    async def deleteAccount(name, context):
        with open('./data/accounts.json') as mainFile:
                file = json.load(mainFile)
                if accountActions.accountBoolean(name) == True:
                    with open('./data/accounts.json') as f:
                        json_file = json.load(f)
                        json_file.pop(name)
                        with open('./data/accounts.json', 'w') as file:
                            json.dump(json_file, file, indent=4)
                            await context.send("Aww.. We are sad to see you going.. ")
                else:
                    await context.send("You don't have an account.. Why are you thinking of deleting it. Its like any number / 0")

class points:
    @staticmethod
    async def pointsCount(name, context):
        with open('./data/accounts.json') as json_file:
            data = json.load(json_file)
            
            if name in data:
                score =  data[name]['points']
                pointsEmbed = discord.Embed(title = f"{name}", description = f"Your score is: `{score}`")
                await context.send(embed = pointsEmbed)
            else:
                await context.send("Oops seems like you don't have an account")
    
    @staticmethod
    async def pointAdd(point, name, ctx):
        if accountActions.accountBoolean(name) == True:
            with open('./data/accounts.json') as file:
                json_data = json.load(file)
                person_folder = json_data[name]
                score = json_data[name]["points"]
                score += point
                person_folder.update({'points' : score})
                with open('./data/accounts.json', 'w') as fileEdit:
                    json.dump(json_data, fileEdit, indent=4)
                    await ctx.send(f"{point} points were added to your account")
        else:
            await ctx.send("**Note : You don't have an account. Therefore the points are not being saved. Create one using this command :  **`!!createac`")
        
    @staticmethod
    async def pointDeduct(point, name):
        if accountActions.accountBoolean(name) == True:
            with open('./data/accounts.json') as file:
                json_data = json.load(file)
                person_folder = json_data[name]
                score = json_data[name]["points"]
                score -= point
                person_folder.update({'points' : score})
                with open('./data/accounts.json', 'w') as fileEdit:
                    json.dump(json_data, fileEdit, indent=4)
        else:
            print("Account Faliure")

class powers:
    @staticmethod
    async def showPowerUps(name, context):
        if accountActions.accountBoolean(name) == True:
            with open('./data/accounts.json') as mainFile:
                file = json.load(mainFile)
                powers = file[name]['powers']
                if powers == []:
                    await context.send("You have no power ups yet.. Try playing some mini games.")
                else:
                    power_embed = discord.Embed(title = "Your powerups")
                    power_embed.set_author(name="Nerd-Bot")
                    for item in sorted(set(powers)):
                        count = powers.count(item)
                        power_embed.add_field(name = item, value = str(count), inline = False)
                    await context.reply(embed = power_embed)
        else:
            await context.send("First create an account using the `!createac` command")

    @staticmethod
    async def addPowerUps(context, power, name, cost):
        if accountActions.accountBoolean(name) == True:
            with open("./data/accounts.json") as mainFile:
                file = json.load(mainFile)
                personal = file[name]
                powerList = file[name]['powers']
                powerList.insert(0, str(power))
                personal.update({"powers" : powerList})
                with open("./data/accounts.json", 'w') as json_data:
                    json.dump(file, json_data, indent = 4)
                    await Embeds.purchaseSuccess(context, power, cost)
        else:
            await context.send("First create an account.. Then only will I be able to add something into your account")  

    @staticmethod
    async def checkPowerUp(power, name):
        if accountActions.accountBoolean(name) == True:
            with open("./data/accounts.json") as ourFile:
                file = json.load(ourFile)
                powerList = file[name]['powerUps']
                if power in powerList:
                    return True
                else:
                    return False
    @staticmethod
    def rainCoin():
        points = random.randint(100, 200)
        return points

class servers:
    @staticmethod
    def addServer(name, id):
        with open("./data/servers.json") as mainFile:
            file = json.load(mainFile)
            new_server = {str(name) : {"id" : int(id), "welcome_channel" : ""}}
            file.update(new_server)
            with open("./data/servers.json", 'w') as fileToEdit:
                json.dump(file, fileToEdit, indent=4)
                
    @staticmethod
    def addWelcome(guild_name,channel_id):
        with open("./data/servers.json") as mainFile:
                file = json.load(mainFile)
                guild_folder = file[guild_name]
                welcome_channel = file[guild_name]["welcome_channel"]
                welcome_channel = channel_id
                guild_folder.update({"welcome_channel" : welcome_channel})
                with open("./data/servers.json", 'w') as fileToEdit:
                    json.dump(file, fileToEdit, indent=4)
    @staticmethod
    def getWelcome(guild_name):
        with open("./data/servers.json") as mainFile:
            file = json.load(mainFile)
            welcome_channel = file[guild_name]["welcome_channel"]
            return (int(welcome_channel))    

class Shop:
    Items = ["Pizza", "Richey Rich", "Rain of Coins", "Nerdy", "Normie", "Obsidion", "Arsenicum", "Radium"]
    
    @staticmethod
    async def shopItem(ctx, name):
        if name in Shop.Items:
            with open("./data/shop.json") as readFile:
                shopItems = json.load(readFile)
                for item in shopItems["shopItems"]:
                    if item["name"] == name:
                        await Embeds.itemEmbed(ctx, name, item["icon"], item["function"], item["cost"])
        else:
            await ctx.reply("Oops. Seems like there's no such item in our shop. Please check available items for sale using the `!shop` command")
    
    @staticmethod
    async def purchase(ctx, name):
        if name in Shop.Items:
            with open("./data/shop.json") as readFile:
                shopItems = json.load(readFile)
                for item in  shopItems["shopItems"]:
                    if item["name"] == name:
                        cost = item["costInt"]
                        break
                await points.pointDeduct(cost, str(ctx.author))
                await powers.addPowerUps(ctx, name, str(ctx.author), cost)
        else:
            await ctx.send("There's no such item in the Nerd Shop. You might want to check the available items using the `!shop` command. Also note we're case-sensitive.")

            

            