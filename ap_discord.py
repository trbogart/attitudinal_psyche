import discord
import logging
import os
import sys
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
        logger.info(f'Command: triads, trifix_or_archetype="{trifix_or_archetype}"')
        result = '\n- '.join(get_triads(trifix_or_archetype.strip()))
        await interaction.response.send_message(result)
    except ValueError as e:
        msg = f"Error: {e}"
        logger.error(msg)
        await interaction.response.send_message(msg)

@bot.tree.command(name="shadow", description="List shadow types, if any, for AP type and subtype")
async def shadow_command(interaction: discord.Interaction, ap_type: str, subtype: str):
    try:
        logger.info(f'Command: shadow, ap_type="{ap_type}", subtype="{subtype}"')
        result = get_shadow_types_str(ap_type.upper().strip(), subtype)
        await interaction.response.send_message(result)
    except ValueError as e:
        msg = f"Error: {e}"
        logger.error(msg)
        await interaction.response.send_message(msg)

@bot.tree.command(name="intertype", description="Show intertype relation between 2 AP types")
async def intertype_command(interaction: discord.Interaction, ap_type1: str, ap_type2: str):
    try:
        logger.info(f'Command: intertype, ap_type1="{ap_type1}", ap_type2="{ap_type2}"')
        result = get_intertype(ap_type1.upper().strip(), ap_type2.upper().strip())
        await interaction.response.send_message(result)
    except ValueError as e:
        msg = f"Error: {e}"
        logger.error(msg)
        await interaction.response.send_message(msg)

@bot.tree.command(name="intertypes", description="List all intertype relations for an AP type")
async def intertypes_command(interaction: discord.Interaction, ap_type: str):
    logger.info(f'Command: intertypes, ap_type="{ap_type}"')
    try:
        relations = [f'Intertype relations for {ap_type.upper()}:']
        for relation, ap_type in get_all_intertypes(ap_type.upper().strip()).items():
            relations.append(f'- {relation}: {ap_type}')
        result = '\n'.join(relations)
        await interaction.response.send_message(result)
    except ValueError as e:
        msg = f"Error: {e}"
        logger.error(msg)
        await interaction.response.send_message(msg)

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stderr)

    FORMAT = '[%(asctime)s] [%(levelname)-8s] %(message)s'
    handler.setFormatter(logging.Formatter(FORMAT))

    logger.addHandler(handler)

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    bot.run(TOKEN)