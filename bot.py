import asyncio
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

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            print(f'Loading cog: {filename} ... ', end='')
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print('SUCCESS')
            
async def main():
    await load()
    await bot.start(TOKEN)
        
asyncio.run(main())