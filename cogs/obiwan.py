import discord
import random
import sqlite3
from discord.ext import commands


class Obiwan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.quotes = []

        with sqlite3.connect("WoT.db") as conn:
            c = conn.cursor()
            for row in c.execute("SELECT quote FROM obiwan"):
                self.quotes.append(row[0])

    @commands.command()
    @commands.guild_only()
    async def obiwan(self, ctx):
        """
        Gives you a quote from the most inspirational man in the galaxy.
        """

        quote = random.choice(self.quotes)
        await ctx.send(f'"{quote}"')

    @commands.Cog.listener()
    async def on_message(self, message):
        # Don't listen to yourself, bot
        if message.author == self.bot.user:
            return

        if message.content.lower() == "hello":
            with open("assets/hello_there.gif", "rb") as f:
                picture = discord.File(f, filename="hello_there.gif")
            await message.reply(file=picture)


async def setup(bot):
    await bot.add_cog(Obiwan(bot))
