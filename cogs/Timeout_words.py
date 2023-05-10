import discord
import sqlite3
from discord.ext import commands


class Timeout_words(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timeout_words = []
        
        
    @commands.command()
    async def add_timeout_word(self, ctx, word: str):
        # Adds a word to the timeout_words table and updates the list in memory
        print(f'Trying to add "{word}" to timeout_words...', end='')
        self.timeout_words.append(word)
        
        try:
            conn = sqlite3.connect("WoT.db")
            c = conn.cursor()
            c.execute("INSERT INTO timeout_words (word) VALUES (?)", (word,))
            conn.commit()
            conn.close()
            print('SUCCESS')
        except Exception as e:
            print(f"Error inserting '{word}' into timeout_words: {e}")
        
        await ctx.send(f"Added '{word}' to the list of timeout words.")
        
        
async def setup(bot):
    await bot.add_cog(Timeout_words(bot))