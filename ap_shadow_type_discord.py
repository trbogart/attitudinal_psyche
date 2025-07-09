import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

from ap_all_intertype import get_all_intertypes
from ap_intertype import get_intertype
from ap_shadow_type_calculator import get_shadow_types_str
from triads import get_triads

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()

@bot.tree.command(name="triads", description='Show triads for Enneagram trifix or EI archetype')
async def triads_command(interaction: discord.Interaction, trifix_or_archetype: str):
    try:
        result = '\n- '.join(get_triads(trifix_or_archetype.strip()))
        await interaction.response.send_message(result)
    except ValueError as e:
        await interaction.response.send_message(f"Error: {e}")


@bot.tree.command(name="shadow", description="List shadow types, if any, for AP type and subtype")
async def shadow_command(interaction: discord.Interaction, ap_type: str, subtype: str):
    try:
        result = get_shadow_types_str(ap_type.upper().strip(), subtype)
        await interaction.response.send_message(result)
    except ValueError as e:
        await interaction.response.send_message(f"Error: {e}")

@bot.tree.command(name="intertype", description="Show intertype relation between 2 AP types")
async def intertype_command(interaction: discord.Interaction, ap_type1: str, ap_type2: str):
    try:
        result = get_intertype(ap_type1.upper().strip(), ap_type2.upper().strip())
        await interaction.response.send_message(result)
    except ValueError as e:
        await interaction.response.send_message(f"Error: {e}")

@bot.tree.command(name="intertypes", description="List all intertype relations for an AP type")
async def intertypes_command(interaction: discord.Interaction, ap_type: str):
    try:
        relations = [f'Intertype relations for {ap_type.upper()}:']
        for relation, ap_type in get_all_intertypes(ap_type.upper().strip()).items():
            relations.append(f'- {relation}: {ap_type}')
        result = '\n'.join(relations)
        await interaction.response.send_message(result)
    except ValueError as e:
        await interaction.response.send_message(f"Error: {e}")

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot.run(TOKEN)