from discord.ext import commands
from .common.dataman import servers
from .common.errors import Errors
import discord


class EventListeners(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await Errors.checkErrors(ctx, error)

    @commands.Cog.listener()
    async def on_ready(self):
        general_channel = self.client.get_channel(858918424125767693)
        await general_channel.send("Hello there!")
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game('Nerdbot'))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = self.client.get_channel(servers.getWelcome(member.guild.name))
        await welcome_channel.send(f"Hello there! {member.mention}. We welcome you to {member.guild.name}. Hope you are having an amazing day.") 
        await member.send(f"Hey {member.mention} :sparkles: :sparkles:.\nWe welcome you to the server. To start with you may use the `!helpc` command to get some commands you can use to interact with me.. Hope you will have fun.. See you there.. Bye until then.. :wave:")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        servers.addServer(guild.name, guild.id)
        general = discord.utils.find(lambda x: x.name == 'general',  guild.text_channels)
        if general and general.permissions_for(guild.me).send_messages:
            await general.send(f'Hello {guild.name}! You all seem to be very excited indeed.. To start with type `!helpc` and just drop by and give a hello to me by `!hello` command.')

    
def setup(client):
    client.add_cog(EventListeners(client))