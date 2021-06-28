from discord.ext import commands
import random
import asyncio
from common.dataman import powers, points

class RandomCommands(commands.Cog):
    rand_sent = ['There is no wind in the football.', 'Why Haircut not cut..?', "Don't stand in front of my back"]
    
    def __init__(self, client):
        self.client = client
    
    '''
    RANDOM SENTENCE TYPING TEST
    '''

    # Creating a list of random sentences

    @commands.command(name="typee")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def typee(self,ctx):
        randomness = random.choice(self.rand_sent)
        channel = ctx.channel
        original_message = await ctx.send(f"Hello {ctx.author.mention}! Welcome to the typing test. Remember the following sentence: `{randomness}`")
        await asyncio.sleep(5)
        await original_message.edit(content = "Now type the sentence which was shown")

        def check(m):
            return m.author == ctx.author and m.channel == channel

        msg = await self.client.wait_for('message', check=check)
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
    @commands.command(name = "rando")    
    async def rando(self,ctx, *args):
        if len(args) == 0 or len(args) == 1:
            await ctx.send("Oops I think you have made a mistake in your commands.. This command only works under the following conditions: \n Your data should have more than one ")
        user_list = args
        random_selection = random.choice(user_list)
        choice = str(random_selection)
        await ctx.send(f'{ctx.author.mention} Your random choice is {choice}')    
        

    '''
    RANDOM REACTION
    '''
    @commands.command(name = "reaction")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def reaction(self,ctx):
        reaction_list = ['👉🏻', '👌', '🤣', '👀', '😒', '👍', '❤', '🙌', '🎂', '🎉', '🙏🏻', '😎', '😡', '😢', '😰']
        challenge_reaction = random.choice(reaction_list)
        await ctx.send(f"Give me this reaction {ctx.author.mention}: {challenge_reaction}")
        def checkReact(r, u):
            return u == ctx.author
        reaction, user = await self.client.wait_for("reaction_add", check=checkReact)
        if str(reaction.emoji) == challenge_reaction:
            await ctx.send(f"Correct answer {user.mention}.")
            await points.pointAdd(20, str(user), ctx)
        else:
            await ctx.send(f"Wrong answer {user.mention}")
            
    '''
    THE REVERSE STRING
    '''
    text_list = ["avatar", "hello", "alliteration", "randomness", "jacob", "wow"]

    @commands.command(name = "word")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def word(self, ctx):
        text = random.choice(self.text_list)
        await ctx.send(f"Hello {ctx.author.mention}! Type this word backwards now! `{text}`.")
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        msg = await self.client.wait_for('message', check=check)
        if str(msg.content) == text[::-1]:
            await ctx.reply(f"Correct answer {msg.author.mention} ")
            if powers.checkPowerUp("Rain of Coins", str(ctx.author)):
                await points.pointAdd(powers.rainCoin(), str(msg.author), ctx)
            else:
                await points.pointAdd(20, str(msg.author), ctx)
        else:
            await ctx.reply(f"Wrong Answer {msg.author.mention}")
                
    
            
def setup(client):
    client.add_cog(RandomCommands(client))