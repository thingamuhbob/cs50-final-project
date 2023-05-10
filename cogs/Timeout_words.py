import discord
import sqlite3
from discord.ext import commands


class Timeout_words(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timeout_words = []
        
        with sqlite3.connect("WoT.db") as conn:
            c = conn.cursor()
            for row in c.execute("SELECT word FROM timeout_words"):
                self.timeout_words.append(row[0])
        print('Timeout words loaded from db.')        
        
        
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def add_timeout_word(self, ctx, word: str):
        # Adds a word to the timeout_words table and updates the list in memory
        word = word.lower()
        if word in self.timeout_words:
            print(f"'{word}' is already on the timeout words list.")
            await ctx.send(f"'{word}' is already on the timeout words list.")
            return
        
        print(f'Trying to add "{word}" to timeout_words... ', end='')
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
        
        
    @add_timeout_word.error
    async def add_timeout_word_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('You do not have the permissions to add a timeout word.')
            
            
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def remove_timeout_word(self, ctx, word: str):
        word = word.lower()
        if word == 'zorfin':
            await ctx.send("Why would you ever want to do that... BUT I GUESS:")
        if word not in self.timeout_words:
            print(f"'{word}' is not on the timeout words list.")
            await ctx.send(f"'{word}' is not on the timeout words list.")
            return
        
        print(f'Trying to remove "{word}" from timeout_words... ', end='')
        self.timeout_words.remove(f'{word}')
        if word in self.timeout_words:
            print(f'timeout_words still contains an instance of {word}')
            
        try:
            conn = sqlite3.connect("WoT.db")
            c = conn.cursor()
            c.execute("DELETE FROM timeout_words WHERE word = ?", (word,))
            conn.commit()
            conn.close()
            print('SUCCESS')
        except Exception as e:
            print(f"Error deleting '{word}' from the timeout_words table: {e}")
            
        await ctx.send(f"Removed '{word}' from the list of timeout words.")
        
    @remove_timeout_word.error
    async def remove_timeout_word_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('You do not have the permissions to remove a timeout word.')
        
        
async def setup(bot):
    await bot.add_cog(Timeout_words(bot))