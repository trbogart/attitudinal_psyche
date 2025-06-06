import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from ap_shadow_type_calculator import get_shadow_types_str

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()

@bot.tree.command(name="shadow", description="Get shadow types")
async def shadow_command(interaction: discord.Interaction, ap_type: str, subtype: str):
    try:
        result = get_shadow_types_str(ap_type.upper(), subtype)
        await interaction.response.send_message(result)
    except ValueError as e:
        await interaction.response.send_message(f"Error: {e}")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot.run(TOKEN)