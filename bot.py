import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True 
intents.members = True 

bot = commands.Bot(command_prefix="!", intents=intents)

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Cog chargé : {filename}")

@bot.event
async def on_ready():
    print(f"{bot.user} est connecté !")
    synced = await bot.tree.sync()
    print(f"{len(synced)} slash command(s) synchronisée(s).")
    
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())