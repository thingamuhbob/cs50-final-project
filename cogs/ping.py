import discord
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """
        Responds with the current bot latency.
        """

        latency = round(self.bot.latency * 1000, 3)
        await ctx.send(f"Pong! \nLatency: {latency}ms")


async def setup(bot):
    await bot.add_cog(Ping(bot))
