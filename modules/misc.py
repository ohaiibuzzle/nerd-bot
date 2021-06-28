from discord.ext import commands
from .common.dataman import servers
from .common.embeds import Embeds
from .common.dataman import accountActions, points
import giphy_client
import random
import discord
import os

class MiscCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.giphy_api_key = os.getenv("GIPHY_TOKEN")
        
    @commands.command(name = "info")
    async def info(self, ctx):
        await Embeds.infoEmbed(ctx)

    @commands.command(name = "setwelcome")
    async def setwelcome(self, ctx):
        servers.addWelcome(ctx.guild.name, ctx.channel.id)
        await ctx.send("This channel is now set as the welcome channel")

    @commands.command(name="helpc")
    async def helpc(self, ctx):
        await Embeds.helpEmbed(ctx)
    '''
    GREETING COMMAND WITH HELLO
    '''
    # keep this command
    @commands.command(name = "hello")
    async def hello(self, ctx):
        channel = ctx.channel
        await ctx.send('Say hello!')

        def check(m):
            return m.content == 'hello' and m.channel == channel

        msg = await self.client.wait_for('message', check=check)
        await ctx.send('Hello {.author.mention}!'.format(msg))


    '''
    DM MESSAGE GAME
    '''
    @commands.command(name = "dmme")
    async def dmme(self, ctx, *args):
        content = " ".join(args) 

        if "".join(args) == "":
            await ctx.send("Oops you made a mistake in writing the command. Here's the syntax for using this particular command: `!dmme [content that you want to be sent to yourself by the bot]`")   

        else:
            await ctx.author.send(f"Hello {ctx.author.mention}. \n {content}")


    '''
    AVATAR RETURN
    '''
    @commands.command(name = "avatar")
    async def avatar(self, ctx):
        async with ctx.channel.typing():
            await Embeds.avatarEmbed(ctx)
        
    '''
    SENDING WHAT THE DEV IS WORKING ON
    '''

    @commands.command(name = "workingon")
    async def workingon(self, ctx):
        async with ctx.channel.typing():
            link = 'https://github.com/amazinglySK/amazinglySK#working-on'
            await ctx.send(f"Check out what our dev is working on in this github page ⌨: \n {link} ")

    '''
    GIF command
    '''

    @commands.command(name = "gif")
    async def gif(self, ctx, *, q = "Smile"):
        async with ctx.channel.typing():
            api_instance = giphy_client.DefaultApi()

            try:
                api_response = api_instance.gifs_search_get(self.giphy_api_key, q, limit = 5, rating = 'g')
                lst = list(api_response.data)
                giff = random.choice(lst)

                gif_embed = discord.Embed(title = q)
                gif_embed.set_image(url = f"https://media.giphy.com/media/{giff.id}/giphy.gif")
                gif_embed.set_author(name = str(ctx.author))

                await ctx.reply(embed = gif_embed)
            
            except giphy_client.rest.ApiException as e:
                print("Something went wrong.")

    '''
    Account Creation
    '''

    @commands.command(name = "createac")
    async def createac(self, ctx):
        Actions_account = accountActions()
        async with ctx.channel.typing():
            await Actions_account.accountCheck(str(ctx.author), ctx)

    '''
    Account deletion
    '''

    @commands.command(name = "deleteac")
    async def deleteac(self, ctx):
        async with ctx.channel.typing():
            await accountActions.deleteAccount(str(ctx.author), ctx)
    '''
    Gives the score as an embed
    '''
    @commands.command(name = "myscore")
    async def myscore(self, ctx):
        async with ctx.channel.typing():
            await points.pointsCount(str(ctx.author), ctx)

def setup(client):
    client.add_cog(MiscCommands(client))