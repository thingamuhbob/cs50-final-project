import os
import datetime
import sqlite3

import discord
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

class Timeout_words(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timeout_words = []
        
    # TODO: load words
    # def load_timeout_words(self):
    #     # Connect to db and fetch timeout_words table
    #     conn = sqlite3.connect('WoT.db')
    #     c = conn.cursor()
    #     c.execute("SELECT")
        
    @commands.command()
    async def add_timeout_word(self, ctx, word: str):
        # Adds a word to the timeout_words table and updates the list in memory
        word = ctx
        self.timeout_words.append(word)
        
        conn = sqlite3.connect('WoT.db')
        c = conn.cursor()
        c.execute("INSERT INTO timeout_words (word) VALUES (?)", word)
        conn.commit()
        
        await ctx.send(f"Added '{word}' to the list of timeout words.")
        
def setup(bot):
    bot.add_cog(Timeout_words(bot))
    
bot.run(TOKEN)