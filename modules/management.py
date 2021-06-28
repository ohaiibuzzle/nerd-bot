from discord.ext import commands
from common.embeds import Embeds

import discord

class ManagementCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(name = "createchannel")
    @commands.is_owner()
    async def createchannel(self, ctx, channel_name = "hi", *category):
        category_coded = discord.utils.get(ctx.guild.categories, name = " ".join(category))
        existing_channel = discord.utils.get(ctx.guild.channels, name = channel_name)
        if not existing_channel:
            msg = await ctx.send(f"Just a sec {ctx.author.mention}. I am creating the text channel")
            await ctx.guild.create_text_channel(channel_name, category = category_coded)
            msg.edit("Done !!")
        else:
            await ctx.send("A channel with this name exists!")

    @commands.command(name = "deletechannel")
    @commands.is_owner()
    async def deletechannel(self, ctx, channel_name):
        existing_channel = discord.utils.get(ctx.guild.channels, name = channel_name)
        if existing_channel:
            org_msg = await ctx.send(f"Just a sec {ctx.author.mention}...")
            await existing_channel.delete()
            await org_msg.edit(content = "Done!!")
        else:
            await ctx.send("A channel with that name doesn't exist.. So why would you delete it?")    
    

    @commands.command(name = "kick")
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason = None):
        await member.kick(reason=reason)
        await Embeds.kickEmbed(ctx, str(member), str(ctx.author))

    @commands.command(name = "ban")
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member, *, reason = None):
        await member.ban(reason=reason)
        await Embeds.banEmbed(ctx, str(member), str(ctx.author))

    @commands.command(name = "unban")
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx, member: discord.Member, *, reason = None):
        await member.unban(reason=reason)
        await Embeds.unBanEmbed(ctx, str(member), str(ctx.author))

def setup(client):
    client.add_cog(ManagementCommands(client))