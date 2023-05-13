import discord
import datetime
import logging
import sqlite3
from discord.ext import commands


class Timeout_words(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # * this is how you get the same logger from the main file
        self.logger = logging.getLogger("discord")
        self.timeout_words = []

        with sqlite3.connect("WoT.db") as conn:
            c = conn.cursor()
            for row in c.execute("SELECT word FROM timeout_words"):
                self.timeout_words.append(row[0])

    @commands.command(usage="add|remove <word>")
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def timeout_word(
        self,
        ctx,
        action: str = commands.parameter(
            default="add", description="The action to perform ('add' or 'remove')."
        ),
        word: str = commands.parameter(
            description="The word to add or remove from the list."
        ),
    ):
        """
        Add or remove a word from the timeout words list.

        Usage:
          $timeout_word <action> <word>
        """

        # Adds a word to the timeout_words table and updates the list in memory
        word = word.lower()
        if action == "add":
            if word in self.timeout_words:
                print(f"'{word}' is already on the timeout words list.")
                await ctx.send(f"'{word}' is already on the timeout words list.")
                return

            print(f'Trying to add "{word}" to timeout_words... ', end="")
            self.timeout_words.append(word)

            try:
                conn = sqlite3.connect("WoT.db")
                c = conn.cursor()
                c.execute("INSERT INTO timeout_words (word) VALUES (?)", (word,))
                conn.commit()
                conn.close()
                print("SUCCESS")
            except Exception as e:
                print(f"Error inserting '{word}' into timeout_words: {e}")

            await ctx.send(f"Added '{word}' to the list of timeout words.")

        elif action == "remove":
            if word == "zorfin":
                await ctx.send("Why would you ever want to do that... BUT I GUESS:")
            if word not in self.timeout_words:
                await ctx.send(f"'{word}' is not on the timeout words list.")
                return
            print(f'Trying to remove "{word}" from timeout_words... ', end="")
            self.timeout_words.remove(word)
            try:
                conn = sqlite3.connect("WoT.db")
                c = conn.cursor()
                c.execute("DELETE FROM timeout_words WHERE word = ?", (word,))
                conn.commit()
                conn.close()
                print("SUCCESS")
            except Exception as e:
                print(f"Error deleting '{word}' from the timeout_words table: {e}")
            await ctx.send(f"Removed '{word}' from the list of timeout words.")
        else:
            await ctx.send("Invalid action. Please use 'add' or 'remove'.")

    @timeout_word.error
    async def timeout_word_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            self.logger.warning(
                f"{ctx.author.name} attempted to run {ctx.command} without proper permissions."
            )
            await ctx.send("You do not have the permissions to edit the timeout words.")

    @commands.Cog.listener()
    async def on_message(self, message):
        # Don't listen to yourself, bot
        if message.author == self.bot.user:
            return

        # Skip command messages
        if message.content.startswith(self.bot.command_prefix):
            return

        for word in self.timeout_words:
            if word in message.content:
                d = datetime.timedelta(seconds=300)
                reason = f"used a timeout word: {word}"
                await message.delete()
                await message.author.timeout(d, reason=reason)
                await message.reply(
                    f"{message.author.name} has been timed out for five minutes for using a naughty word."
                )

    @commands.command()
    async def timeout_list(self, ctx):
        """
        Shows a list of the current timeout words.
        """
        lst = ""
        bullet = "\u2022"
        for word in self.timeout_words:
            lst += f"{bullet} {word}\n"
        await ctx.send(f"__Timeout words:__\n{lst}")


async def setup(bot):
    await bot.add_cog(Timeout_words(bot))
