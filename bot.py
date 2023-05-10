import os
import datetime
import sqlite3

import discord
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    # TODO: figure out guilds already connected to
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    # print(f'')
    print('------')
        
    
class Timeout_words(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.timeout_words
        
    def load_timeout_words(self):
        # Connect to WoT.db file
        conn = sqlite3.connect('WoT.db')
        c = conn.cursor()

        c.execute('''SELECT servers.server_id, timeout_words.word
                  FROM servers
                  JOIN server_timeout_word ON servers.id = server_timeout_word.server_id
                  JOIN timeout_words ON server_timeout_word.timeout_word_id - timeout_words.id;''')
        
            
    @commands.Cog.listener()
    async def on_message(self, message):
        # Don't listen to yourself, bot
        if message.author == bot.user:
            return 
        
    @commands.command()
    async def add_timeout_word(self, ctx, word: str):
        server_id = ctx.guild.id
        word = ctx
        
# Cog registration
bot.add_cog(Timeout_words(bot))
        
bot.run(TOKEN)