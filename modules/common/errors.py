import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from .embeds import Embeds

class Errors:
    @staticmethod
    async def checkErrors(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            if round(error.retry_after) < 60:
                await Embeds.errorEmbed(ctx, "Timeout :alarm_clock:", f"Woah... Calm down bro.. Wait for more {round(error.retry_after)}s to use this again")
            else:
                minutes = error.retry_after//60
                sec = error.retry_after%60
                await Embeds.errorEmbed(ctx, "Timeout :alarm_clock:", f"Woah... Calm down bro.. Wait for more {minutes}mins and {sec}secs to use this again")
        if isinstance(error, commands.NotOwner):
            await Embeds.errorEmbed(ctx, "Owner perm missing","Sorry.. but this command is exclusively for the server owners.")
        if isinstance(error, commands.CommandNotFound):
            await Embeds.errorEmbed(ctx, "Command Error", "Hey.. Seems like a command with this name doesn't exist. You may want some help.. Type this command to get a list of all commands `!helpc`")  
        if isinstance(error, commands.MissingPermissions):
            await Embeds.errorEmbed(ctx, "Permission Error", "Hey you don't have the permission to kick someone out of the server.")
