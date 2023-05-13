import discord, logging, random
from discord.ext import commands


class Coin_flip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.coinflip_user = None

    @commands.command()
    async def coinflip(self, ctx):
        """
        Flip a coin. Guess heads or tails.
        """
        if self.coinflip_user is not None:
            await ctx.send(
                "A game is already in progress. Please wait for it to finish."
            )
            return

        self.coinflip_user = ctx.author.id
        with open("assets/coinflip.gif", "rb") as f:
            gif = discord.File(f)
        await ctx.send(
            f"Okay, {ctx.author.name}, I'm going to flip a coin. You call heads or tails.\n\n Use $guess <heads | tails> to guess.",
            file=gif,
        )

    @commands.command()
    async def guess(
        self, ctx, guess: str = commands.parameter(description="<heads | tails>")
    ):
        """
        Make a guess for the coinflip game.
        """
        if self.coinflip_user is None:
            await ctx.send(
                "No game is currently in progress. Use $coinflip to start a new game."
            )
            return

        if ctx.author.id != self.coinflip_user:
            await ctx.send(
                "You cannot make a guess for this game. Please wait for the current player to finish."
            )
            return

        guess = guess.lower()
        if guess != "heads" and guess != "tails":
            await ctx.send("Invalid guess. Please guess either 'heads' or 'tails'.")
            return

        result = random.choice(["heads", "tails"])
        if guess == result:
            await ctx.send(f"{ctx.author.name} wins! It landed on {result}.")
        else:
            await ctx.send(f"{ctx.author.name} loses! It landed on {result}.")

        self.coinflip_user = None

    @guess.error
    async def guess_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            self.logger.error(
                f"{ctx.author.name} attempted to ${ctx.command} without an argument"
            )
            await ctx.send("You must include either 'heads' or 'tails' after $guess")


async def setup(bot):
    await bot.add_cog(Coin_flip(bot))
