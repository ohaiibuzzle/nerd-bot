import discord
from discord.ext import commands
import random
import asyncio
import json
import giphy_client
from giphy_client.rest import ApiException
from acmanager import accountActions
from point import points


file = open('data.json', 'r')
r = json.loads(file.read())

'''
Making some code that will extract the API key from the txt file
'''

TOKEN = r['discord_token']

'''
Making some code to get the giphy token
'''
global giphy_api_key
giphy_api_key = r['giphy_token']


client = commands.Bot(command_prefix="!!")


@client.event
async def on_ready():
    general_channel = client.get_channel(825307555088957450)
    await general_channel.send("Hello there!!")
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Nerdbot'))

@client.command(name="commands")
async def commands(context):
    commands_embed = discord.Embed(title="Commands", description="Try out these possible commands")
    commands_embed.add_field(name="Command prefix: ", value="`!!` (Don't forget to include this before all your commands)", inline= False)
    commands_embed.add_field(name="For random selector: ", value = "!!rando `[give some random names of things without a comma]`", inline= False)
    commands_embed.add_field(name="For a hello request: ", value = "`!!hello`", inline = False)
    commands_embed.add_field(name = "For a typing task:", value = "`!!reaction`", inline = False )
    commands_embed.add_field(name = "For getting a DM message from the bot", value = "!!dmme [write what you want to get as DM]", inline=False)

    await context.send(embed = commands_embed)

'''
GREETING COMMAND WITH HELLO
'''
# keep this command
@client.command(name = "hello")
async def typing(context):
    channel = context.channel
    await context.send('Say hello!')

    def check(m):
        return m.content == 'hello' and m.channel == channel

    msg = await client.wait_for('message', check=check)
    await context.send('Hello {.author.mention}!'.format(msg))


'''
RANDOM SENTENCE TYPING TEST
'''

# Creating a list of random sentences
rand_sent = ['There is no wind in the football.', 'Why Haircut not cut..?', "Don't stand in front of my back"]
@client.command(name="typee")
async def typee(context):
    randomness = random.choice(rand_sent)
    channel = context.channel
    original_message = await context.send(f"Hello {context.author.mention}! Welcome to the typing test. Remember the following sentence: `{randomness}`")
    await asyncio.sleep(5)
    await original_message.edit(content = "Now type the sentence which was shown")

    def check(m):
        return m.content == randomness and m.channel == channel

    msg = await client.wait_for('message', check=check)
    await context.send('Correct answer {.author.mention}!'.format(msg))

# Keep this command
'''
RANDOM GENERATOR
'''
@client.command(name = "rando")    
async def rando(context, *args):
    if len(args) == 0 or len(args) == 1:
        await context.send("Oops I think you have made a mistake in your commands.. This command only works under the following conditions: \n Your data should have more than one ")
    user_list = args
    random_selection = random.choice(user_list)
    choice = str(random_selection)
    await context.send(f'{context.author.mention} Your random choice is {choice}')    
    

'''
RANDOM REACTION
'''
@client.command(name="reaction")
async def reaction(context):
    reactions = ['👉🏻', '👌', '✌', '🤣', '👀', '😒', '👍', '❤', '🙌', '🎂', '🎉', '🙏🏻', '😎', '😡', '😢', '😰']
    global random_reaction
    random_reaction = random.choice(reactions)
    await context.send(f"Give me this reaction {random_reaction}")
    @client.event
    async def on_reaction_add(reaction, user):
        if str(reaction) == str(random_reaction):
            await context.send(f'{context.author.mention} You are amazing in memorizing. Keep it up buddy')
        else:
            await context.send(f'Oops {context.author.mention}! You made a mistake. Please try again later.')

'''
DM MESSAGE GAME
'''
@client.command(name = "dmme")
async def dmme(context, *args):
    content = " ".join(args) 

    if "".join(args) == "":
        await context.send("Oops you made a mistake in writing the command. Here's the syntax for using this particular command: `!!dmme [content that you want to be sent to yourself by the bot]`")   

    else:
        await context.author.send(f"Hello {context.author.mention}. \n {content}")


'''
AVATAR RETURN
'''
@client.command(name = "avatar")
async def avatar(context):
    a_link =  context.author.avatar_url
    e = discord.Embed()
    e.set_image(url = a_link)
    await context.send(f"Hello {context.author.mention}!! Heres your avatar \n", embed = e)
    print(str(context.author))


'''
THE REVERSE STRING
'''
text_list = ["avatar", "hello", "alliteration", "randomness", "jacob", "wow"]

@client.command(name = "word")
async def word(context):
    text = random.choice(text_list)
    await context.send(f"Hello {context.author.mention}!! Type this word backwards now!! `{text}`.")

    async def check(m):
        if m.content == text[::-1]:
            await context.send('Correct answer {.author.mention}!'.format(msg))
        else:
            await context.send('Oops {.author.mention}!'.format(msg))


    msg = await client.wait_for('message', check=check)
    
'''
SENDING WHAT THE DEV IS WORKING ON
'''

@client.command(name = "workingon")
async def workingon(context):
    link = 'https://github.com/amazinglySK/amazinglySK#working-on'
    await context.send(f"Check out what our dev is working on in this github page ⌨: \n {link} ")

'''
WEBSITE LINK
'''
@client.command(name = "website")
async def website(context):
    website = 'https://amazinglysk.github.io/nerd-bot-website/'
    await context.send(f"Check out our latest news and info at this website: {link}")

@client.command(name = "gif")
async def gif(context, *, q = "Smile"):
    api_instance = giphy_client.DefaultApi()

    try:
        api_response = api_instance.gifs_search_get(giphy_api_key, q, limit = 5, rating = 'g')
        lst = list(api_response.data)
        giff = random.choice(lst)

        gif_embed = discord.Embed(title = q)
        gif_embed.set_image(url = f"https://media.giphy.com/media/{giff.id}/giphy.gif")
        gif_embed.set_author(name = context.author.mention)

        await context.send(embed = gif_embed)
    
    except ApiException as e:
        print("Something went wrong.")

'''
Account Creation
'''

@client.command( name = "createac")
async def createac(context):
    await accountActions.accountCheck(accountActions, str(context.author), context)


@client.command(name = "deleteac")
async def deleteac(context):
    await accountActions.deleteAccount(str(context.author), context)

@client.command(name = "myscore")
async def myscore(context):
    await points.pointsCount(str(context.author), context)

    
client.run(str(TOKEN))
