import asyncio, discord, logging, os

from discord.ext import commands
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

# get private token from .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.guild_messages = True
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="$", case_insensitive=True, intents=intents)

# LOGGING
# Define the rotating file handler
log_handler = RotatingFileHandler(
    filename="bot.log", maxBytes=32 * 1024 * 1024, backupCount=5, encoding="utf-8"
)
# Set the log level and add the handler to the logger
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
dt_fmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(
    "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
)
log_handler.setFormatter(formatter)


# Is bot loaded?
@bot.event
async def on_ready():
    print("------")
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


# Load cogs
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            print(f"Loading cog: {filename} ... ", end="")
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print("SUCCESS")


# Wretched hive of scum and villainy
@bot.event
async def on_message(message):
    # Don't listen to yourself, bot
    if message.author == bot.user:
        return

    if "wipes on trash" in message.content.lower():
        await message.reply(
            "Wipes on Trash. You will never find a more wretched hive of scum and villainy. We must be cautious."
        )

    await bot.process_commands(message)


# Set up bot
async def main():
    discord.utils.setup_logging(handler=log_handler, formatter=formatter)
    await load()
    await bot.start(TOKEN)


asyncio.run(main())
