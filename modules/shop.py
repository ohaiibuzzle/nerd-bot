from discord.ext import commands
from common.embeds import Embeds
from common.dataman import Shop, powers

class ShopCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.command(name = "shop")
    async def shop(self, ctx):
        await Embeds.shopEmbed(ctx)

    @commands.command(name = "item")
    async def item(self, ctx, *name):
        await Shop.shopItem(ctx, " ".join(name))

    @commands.command(name = "buy")
    async def buy(self, ctx, *, name):
        await Shop.purchase(ctx, name)

    @commands.command(name = "inventory")
    async def inventory(self, ctx):
        await ctx.send("hello")
        await powers.showPowerUps(str(ctx.author), ctx)
    
def setup(client):
    client.add_cog(Shop(client))