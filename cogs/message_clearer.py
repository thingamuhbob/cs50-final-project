import datetime
from discord.ext import tasks, commands

# Run at 11am UTC (6am CDT)
time = datetime.time(hour=11)


class MessageClearer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clear_channel.start()

    def cog_unload(self):
        self.clear_channel.cancel()

    @tasks.loop(time=time)
    async def clear_channel(self):
        # WoT voice-relevant channel
        channel_id = 914748445812723752
        channel = self.bot.get_channel(channel_id)

        if channel:
            await channel.purge(reason="Daily purge")


async def setup(bot):
    await bot.add_cog(MessageClearer(bot))
