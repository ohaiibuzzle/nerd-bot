# Importing Files

import discord
from discord import Member, embeds
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext.commands.cooldowns import BucketType
import random
import asyncio
import json
import giphy_client
from giphy_client.rest import ApiException
from bs4 import BeautifulSoup
import requests
import youtube_dl
import os
from dotenv import load_dotenv
from dataman import *
from errors import Errors
from embeds import Embeds


# Discord intents
intents = discord.Intents.default()
intents.members = True
intents.presences = True

# Loading essential tokens for APIs

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
global giphy_api_key
giphy_api_key = os.getenv("GIPHY_TOKEN")


client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_command_error(ctx, error):
    await Errors.checkErrors(ctx, error)

@client.event
async def on_ready():
    general_channel = client.get_channel(844929006339620935)
    await general_channel.send("Hello there!")
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Nerdbot'))

@client.event
async def on_member_join(member):
    welcome_channel = client.get_channel(servers.getWelcome(member.guild.name))
    await welcome_channel.send(f"Hello there! {member.mention}. We welcome you to {member.guild.name}. Hope you are having an amazing day.") 
    await member.send(f"Hey {member.mention} :sparkles: :sparkles:.\nWe welcome you to the server. To start with you may use the `!helpc` command to get some commands you can use to interact with me.. Hope you will have fun.. See you there.. Bye until then.. :wave:")

@client.event
async def on_guild_join(guild):
    servers.addServer(guild.name, guild.id)
    general = discord.utils.find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send(f'Hello {guild.name}! You all seem to be very excited indeed.. To start with type `!helpc` and just drop by and give a hello to me by `!hello` command.')

@client.command(name = "info")
async def info(ctx):
    await Embeds.infoEmbed(ctx)

@client.command(name = "setwelcome")
async def setwelcome(ctx):
    servers.addWelcome(ctx.guild.name, ctx.channel.id)
    await ctx.send("This channel is now set as the welcome channel")

    

@client.command(name="helpc")
async def helpc(ctx):
    await Embeds.helpEmbed(ctx)
'''
GREETING COMMAND WITH HELLO
'''
# keep this command
@client.command(name = "hello")
async def hello(ctx):
    channel = ctx.channel
    await ctx.send('Say hello!')

    def check(m):
        return m.content == 'hello' and m.channel == channel

    msg = await client.wait_for('message', check=check)
    await ctx.send('Hello {.author.mention}!'.format(msg))


'''
RANDOM SENTENCE TYPING TEST
'''

# Creating a list of random sentences
rand_sent = ['There is no wind in the football.', 'Why Haircut not cut..?', "Don't stand in front of my back"]
@client.command(name="typee")
@commands.cooldown(1, 60, commands.BucketType.user)
async def typee(ctx):
    randomness = random.choice(rand_sent)
    channel = ctx.channel
    original_message = await ctx.send(f"Hello {ctx.author.mention}! Welcome to the typing test. Remember the following sentence: `{randomness}`")
    await asyncio.sleep(5)
    await original_message.edit(content = "Now type the sentence which was shown")

    def check(m):
        return m.author == ctx.author and m.channel == channel

    msg = await client.wait_for('message', check=check)
    if str(msg.content) == str(randomness):
        await ctx.reply(f'Correct answer {msg.author.mention}!')
        if await powers.checkPowerUp("Rain of Coins", str(msg.author)):
            await points.pointAdd(powers.rainCoin(), str(msg.author), ctx)
        else:
            await points.pointAdd(20, str(msg.author), ctx)
    else:
        await ctx.reply(f"Oops you made a mistake {msg.author.mention}")

# Keep this command
'''
RANDOM GENERATOR
'''
@client.command(name = "rando")    
async def rando(ctx, *args):
    if len(args) == 0 or len(args) == 1:
        await ctx.send("Oops I think you have made a mistake in your commands.. This command only works under the following conditions: \n Your data should have more than one ")
    user_list = args
    random_selection = random.choice(user_list)
    choice = str(random_selection)
    await ctx.send(f'{ctx.author.mention} Your random choice is {choice}')    
    

'''
RANDOM REACTION
'''
@client.command(name = "reaction")
@commands.cooldown(1, 60, commands.BucketType.user)
async def reaction(ctx):
    reaction_list = ['👉🏻', '👌', '🤣', '👀', '😒', '👍', '❤', '🙌', '🎂', '🎉', '🙏🏻', '😎', '😡', '😢', '😰']
    challenge_reaction = random.choice(reaction_list)
    await ctx.send(f"Give me this reaction {ctx.author.mention}: {challenge_reaction}")
    def checkReact(r, u):
        return u == ctx.author
    reaction, user = await client.wait_for("reaction_add", check=checkReact)
    if str(reaction.emoji) == challenge_reaction:
        await ctx.send(f"Correct answer {user.mention}.")
        await points.pointAdd(20, str(user), ctx)
    else:
        await ctx.send(f"Wrong answer {user.mention}")

'''
DM MESSAGE GAME
'''
@client.command(name = "dmme")
async def dmme(ctx, *args):
    content = " ".join(args) 

    if "".join(args) == "":
        await ctx.send("Oops you made a mistake in writing the command. Here's the syntax for using this particular command: `!dmme [content that you want to be sent to yourself by the bot]`")   

    else:
        await ctx.author.send(f"Hello {ctx.author.mention}. \n {content}")


'''
AVATAR RETURN
'''
@client.command(name = "avatar")
async def avatar(ctx):
    await Embeds.avatarEmbed(ctx)


'''
THE REVERSE STRING
'''
text_list = ["avatar", "hello", "alliteration", "randomness", "jacob", "wow"]

@client.command(name = "word")
@commands.cooldown(1, 60, commands.BucketType.user)
async def word(ctx):
    text = random.choice(text_list)
    await ctx.send(f"Hello {ctx.author.mention}! Type this word backwards now! `{text}`.")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    msg = await client.wait_for('message', check=check)
    if str(msg.content) == text[::-1]:
        await ctx.reply(f"Correct answer {msg.author.mention} ")
        if powers.checkPowerUp("Rain of Coins", str(ctx.author)):
            await points.pointAdd(powers.rainCoin(), str(msg.author), ctx)
        else:
            await points.pointAdd(20, str(msg.author), ctx)
    else:
        await ctx.reply(f"Wrong Answer {msg.author.mention}")
    
    
'''
SENDING WHAT THE DEV IS WORKING ON
'''

@client.command(name = "workingon")
async def workingon(ctx):
    link = 'https://github.com/amazinglySK/amazinglySK#working-on'
    await ctx.send(f"Check out what our dev is working on in this github page ⌨: \n {link} ")

'''
GIF command
'''

@client.command(name = "gif")
async def gif(ctx, *, q = "Smile"):
    api_instance = giphy_client.DefaultApi()

    try:
        api_response = api_instance.gifs_search_get(giphy_api_key, q, limit = 5, rating = 'g')
        lst = list(api_response.data)
        giff = random.choice(lst)

        gif_embed = discord.Embed(title = q)
        gif_embed.set_image(url = f"https://media.giphy.com/media/{giff.id}/giphy.gif")
        gif_embed.set_author(name = str(ctx.author))

        await ctx.reply(embed = gif_embed)
    
    except ApiException as e:
        print("Something went wrong.")

'''
Account Creation
'''

@client.command( name = "createac")
async def createac(ctx):
    Actions_account = accountActions()
    await Actions_account.accountCheck(str(ctx.author), ctx)

'''
Account deletion
'''

@client.command(name = "deleteac")
async def deleteac(ctx):
    await accountActions.deleteAccount(str(ctx.author), ctx)
'''
Gives the score as an embed
'''
@client.command(name = "myscore")
async def myscore(ctx):
    await points.pointsCount(str(ctx.author), ctx)

'''
Returns a quadratic polynomial with the given zeroes
'''
@client.command(name = "polynomial")
async def polynomial(ctx, alpha, beta):
    user_sum = int(alpha) + int(beta) # Finding the sum
    product = int(alpha) * int(beta) # Fiding the product
    poly = f"x^2 - ({user_sum}) + ({product})" # Using the formula (x^2 - [alpha + beta] + [alpha*beta])
    await ctx.reply(f"Here's your polynomial: {poly} \n Now don't complaint about the -ve signs. Do them on your own!")


'''
The wiki searcher
'''

@client.command(name = "wiki")
async def wiki(ctx, *args):
    topic = "_".join(args)
    inpuUrl = f"https://en.wikipedia.org/wiki/{topic}"
    page = requests.get(url = inpuUrl)
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.find(id="content").find('p', class_ = "")
    await ctx.reply(f"{content.text.strip()[0:500]}... \nTo read the entire article Go here : {inpuUrl}")

'''
Meriam Webster WOD
'''
@client.command(name = "vocab")
async def vocab(ctx):
    mw_url = "https://www.merriam-webster.com/word-of-the-day"
    page = requests.get(url = mw_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    content = soup.find('h1', class_="")
    meaning = []
    for i in soup.find_all("p"):
        meaning.append(i.get_text().strip())
    info = "\n".join(meaning[0:2])
    await ctx.send(f"{content.text.strip()} \nSome information: \n {info} \n For more info go here {mw_url}")

'''
Admin Create Channel
'''
@client.command(name = "createchannel")
@commands.is_owner()
async def createchannel(ctx, channel_name = "hi", *category):
    category_coded = discord.utils.get(ctx.guild.categories, name = " ".join(category))
    existing_channel = discord.utils.get(ctx.guild.channels, name = channel_name)
    if not existing_channel:
        msg = await ctx.send(f"Just a sec {ctx.author.mention}. I am creating the text channel")
        await ctx.guild.create_text_channel(channel_name, category = category_coded)
        msg.edit("Done !!")
    else:
        await ctx.send("A channel with this name exists!")

'''
Admin Delete Channel
'''
@client.command(name = "deletechannel")
@commands.is_owner()
async def deletechannel(ctx, channel_name):
    existing_channel = discord.utils.get(ctx.guild.channels, name = channel_name)
    if existing_channel:
        org_msg = await ctx.send(f"Just a sec {ctx.author.mention}...")
        await existing_channel.delete()
        await org_msg.edit(content = "Done!!")
    else:
        await ctx.send("A channel with that name doesn't exist.. So why would you delete it?")

'''
Kick / Ban / Unban Members
'''
@client.command(name = "kick")
@has_permissions(kick_members = True)
async def kick(ctx, member: discord.Member, *, reason = None):
    await member.kick(reason=reason)
    await Embeds.kickEmbed(ctx, str(member), str(ctx.author))

@client.command(name = "ban")
@has_permissions(ban_members = True)
async def kick(ctx, member: discord.Member, *, reason = None):
    await member.ban(reason=reason)
    await Embeds.banEmbed(ctx, str(member), str(ctx.author))

@client.command(name = "unban")
@has_permissions(ban_members = True)
async def unban(ctx, member: discord.Member, *, reason = None):
    await member.unban(reason=reason)
    await Embeds.unBanEmbed(ctx, str(member), str(ctx.author))

'''
Voice Commands
'''
@client.command()
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='General')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

'''
Shop Commands
'''
@client.command(name = "shop")
async def shop(ctx):
    await Embeds.shopEmbed(ctx)

@client.command(name = "item")
async def item(ctx, *name):
    await Shop.shopItem(ctx, " ".join(name))

@client.command(name = "buy")
async def buy(ctx, *, name):
    await Shop.purchase(ctx, name)

@client.command(name = "inventory")
async def inventory(ctx):
    await ctx.send("hello")
    await powers.showPowerUps(str(ctx.author), ctx)

client.run(str(TOKEN))