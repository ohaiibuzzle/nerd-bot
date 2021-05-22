import discord
from discord import embeds
from discord import colour
from discord.embeds import Embed
from discord.errors import flatten_error_dict
from discord.ext import commands
import time

class Embeds:
    async def helpEmbed(ctx):
        commands_embed = discord.Embed(title="Commands", description="Try out these possible commands", color = 0xffa00f)
        commands_embed.add_field(name="Command prefix: ", value="`!` (Don't forget to include this before all your commands)")
        commands_embed.add_field(name="For random selector: ", value = "!rando `[give some random names of things without a comma]`")
        commands_embed.add_field(name="For a hello request: ", value = "`!hello`")
        commands_embed.add_field(name = "For a typing task:", value = "`!reaction`")
        commands_embed.add_field(name = "For getting a DM message from the bot", value = "!dmme [write what you want to get as DM]")
        commands_embed.add_field(name = "For a wikipedia search:", value = "`!wiki [Write the topic which you want to search.. Wihtout the 'w' words]`")
        commands_embed.add_field(name = "To get your avatar as an image:", value = "`!avatar`")
        commands_embed.add_field(name = "To see what our dev is working on:", value = "`!workingon`")
        commands_embed.add_field(name = "To check out our website:", value = "`!website`")
        commands_embed.add_field(name = "Create your account to earn points ", value = "!`createac`")
        commands_embed.add_field(name = "Delete your account: [Not recommended]", value = "`!deleteac`")
        commands_embed.add_field(name = "Checkout your score:", value = "`!myscore`")
        commands_embed.add_field(name = "Get a random gif:", value = "`!gif [Any emotion eg. Smile, happy etc.]`")
        commands_embed.add_field(name = "Get a quadratic polynomial with its zeroes", value = "`!polynomial [alpha] [beta] {Here alpha and beta are the zeroes. give a space between them}`")
        await ctx.send(embed = commands_embed)
        if ctx.guild.owner_id == ctx.author.id:
            owner_commands = discord.Embed(title = "Owner Specific Commands", color = 0xffa00f)
            owner_commands.add_field(name = "To create a new channel", value = "`!createchannel [name] [category]`")
            owner_commands.add_field(name = "To delete a channel", value = "`!deletechannel [name]`")
            owner_commands.add_field(name = "To set a channel as the welcome channel", value = "`!setwelcome`")
            await ctx.author.send(embed = owner_commands)
        
    async def avatarEmbed(ctx):
        a_link =  ctx.author.avatar_url
        e = discord.Embed(title = f"{str(ctx.author)}'s profile picture", colour = 0x00FF00)
        e.set_image(url = a_link)
        await ctx.reply(f"Hello {ctx.author.mention}! Heres your avatar \n", embed = e)
    
    async def shopEmbed(ctx):
        shop_embed = discord.Embed(title = "Nerd Shop", colour = 0xF0FFF0)
        shop_embed.add_field(name = ":pizza: *Pizza*", value = "1200 :coin:", inline=False)
        shop_embed.add_field(name = ":crown: *Richey Rich*", value = "10,000 :coin:", inline=False)
        shop_embed.add_field(name = ":moneybag: *Rain of coins*", value = "500 :coin:", inline=False)
        shop_embed.add_field(name = ":book: *Nerdy*", value = "500 :coin:", inline=False)
        shop_embed.add_field(name = "Normie :package:", value = "500 :coin:", inline=False)
        shop_embed.add_field(name = "Obsidion :package:", value = "1000 :coin:", inline=False)
        shop_embed.add_field(name = "Arsenicum :package:", value = "2000 :coin:", inline=False)
        shop_embed.add_field(name = "Radium :package:", value = "3000 :coin:", inline=False)
        await ctx.reply(embed = shop_embed)
    
    async def itemEmbed(ctx, name, icon,function, cost):
        item_embed = discord.Embed(title = name, colour = 0xF0FFF0)
        item_embed.add_field(name = "Name:", value = name, inline = False)
        item_embed.add_field(name = "Icon:", value = icon )
        item_embed.add_field(name = "Function:", value = function, inline = False)
        item_embed.add_field(name = "Cost:", value = cost, inline = False)
        item_embed.set_author(name = "Nerd Bot")
        item_embed.set_footer(text = "For more in depth info about each of the items in the shop ---> `!item <item name>`")
        await ctx.reply(embed = item_embed)

    async def kickEmbed(ctx, name, author):
        t = time.localtime()
        ban_embed = discord.Embed(title = f"{name} is kicked now by {author}", color = 0xFF0000)
        ban_embed.add_field(name = "Kicked", value = name)
        ban_embed.add_field(name = "Time", value = time.strftime("%H:%M:%S", t))
        ban_embed.add_field(name = "Initiator", value = author)
        await ctx.send(embed = ban_embed)
    
    async def banEmbed(ctx, name, author):
        t = time.localtime()
        ban_embed = discord.Embed(title = f"{name} is banned now by {author}", colour = 0xFF0000)
        ban_embed.add_field(name = "Banned", value = name)
        ban_embed.add_field(name = "Time", value = time.strftime("%H:%M:%S", t))
        ban_embed.add_field(name = "Initiator", value = author)
        await ctx.send(embed = ban_embed)

    async def unBanEmbed(ctx, name, author):
        t = time.localtime()
        ban_embed = discord.Embed(title = f"{name} is unbanned now by {author}", color = 0xFFFFFF)
        ban_embed.add_field(name = "Unbanned", value = name)
        ban_embed.add_field(name = "Time", value = time.strftime("%H:%M:%S", t))
        ban_embed.add_field(name = "Initiator", value = author)
        await ctx.send(embed = ban_embed)

    async def errorEmbed(ctx, error_name, error):
        error_embed = discord.Embed(title = ":x: Error", color = 0xff0000)
        error_embed.add_field(name = "Error name:", value = error_name, inline=False)
        error_embed.add_field(name = "Error message", value = error)
        await ctx.reply(embed = error_embed)

    async def powerEmbed(ctx, data):
        power_embed = discord.Embed(title = "Your powerups", color = 0xFFA500)
        power_embed.add_field(name = "Powers")
        await ctx.reply(embed = power_embed)
    
    async def purchaseSuccess(ctx, power, cost):
        t = time.localtime()
        success_msg = discord.Embed(title = ":ok: Purchase summary", color = 0x00FF00)
        success_msg.add_field(name = "Power up added :", value = power)
        success_msg.add_field(name = "Cost: ", value = cost )
        success_msg.add_field(name = "Time: ", value = time.strftime("%H:%M:%S", t))
        await ctx.reply(embed = success_msg)
    
    async def infoEmbed(ctx):
        info_embed = discord.Embed(title = "NERDBOT", description = "Some useful information about nerdbot", colour = 0xF0FFF0)
        info_embed.add_field(name = "Version : ", value = ":sparkles: v1.0.0 :sparkles:", inline = False)
        info_embed.add_field(name = "Date of launch : ", value = "22/05/21", inline = False)
        info_embed.add_field(name = "Help command", value = "`helpc`", inline = False)
        info_embed.add_field(name = "Launch name : ", value = "Getting started!!", inline = False)
        info_embed.set_thumbnail(url = "https://cdn.discordapp.com/app-icons/818167692929663038/f648f297606ae47db263f3bad2b02bfe.png?size=256")
        await ctx.reply(embed = info_embed)