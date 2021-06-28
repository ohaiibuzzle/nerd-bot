from discord.ext import commands
from bs4 import BeautifulSoup
import aiohttp

class WebCommands(commands.Cog):
    timeout = aiohttp.ClientTimeout(total=15)
    
    def __init__(self, client):
        self.client = client
    
    '''
    The wiki searcher
    '''

    @commands.command(name = "wiki")
    async def wiki(self, ctx, *args):
        async with ctx.channel.typing():
            topic = "_".join(args)
            inpuUrl = f"https://en.wikipedia.org/wiki/{topic}"
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                page = await session.get(url = inpuUrl)
                soup = BeautifulSoup(await page.read(), 'html.parser')
                content = soup.find(id="content").find('p', class_ = "")
                await ctx.reply(f"{content.text.strip()[0:500]}... \nTo read the entire article Go here : {inpuUrl}")

    '''
    Meriam Webster WOD
    '''
    @commands.command(name = "vocab")
    async def vocab(self, ctx):
        async with ctx.channel.typing():
            mw_url = "https://www.merriam-webster.com/word-of-the-day"
            
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                page = await session.get(url = mw_url)
                soup = BeautifulSoup(await page.read(), 'html.parser')
                content = soup.find('h1', class_="")
                meaning = []
                for i in soup.find_all("p"):
                    meaning.append(i.get_text().strip())
                info = "\n".join(meaning[0:2])
                await ctx.send(f"{content.text.strip()} \nSome information: \n {info} \n For more info go here {mw_url}")
            
def setup(client):
    client.add_cog(WebCommands(client))