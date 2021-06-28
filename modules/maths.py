from discord.ext import commands

class MathCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    '''
    Returns a quadratic polynomial with the given zeroes
    '''
    @commands.command(name = "polynomial")
    async def polynomial(self, ctx, alpha, beta):
        user_sum = int(alpha) + int(beta) # Finding the sum
        product = int(alpha) * int(beta) # Fiding the product
        poly = f"x^2 - ({user_sum}) + ({product})" # Using the formula (x^2 - [alpha + beta] + [alpha*beta])
        await ctx.reply(f"Here's your polynomial: {poly} \n Now don't complaint about the -ve signs. Do them on your own!")
    
def setup(client):
    client.add_cog(MathCommands(client))