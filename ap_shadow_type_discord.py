import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from ap_shadow_type_calculator import get_shadow_types_str

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def shadow(ctx, ap_type: str, subtype: str):
    try:
        result = get_shadow_types_str(ap_type.upper(), subtype)
        await ctx.send(result)
    except ValueError as e:
        await ctx.send(f'Error: {e}')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot.run(TOKEN)