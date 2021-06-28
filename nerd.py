# Importing Files
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

# Discord intents
intents = discord.Intents.default()
intents.members = True
intents.presences = True

# Loading essential tokens for APIs

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
client = commands.Bot(command_prefix="!", intents=intents)

client.load_extension('modules.event_listeners')
client.load_extension('modules.management')
client.load_extension('modules.maths')
client.load_extension('modules.misc')
client.load_extension('modules.randoms')
client.load_extension('modules.shop')
client.load_extension('modules.voice')
client.load_extension('modules.web')

client.run(str(TOKEN))