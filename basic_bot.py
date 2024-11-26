import json
import os
import discord
from discord.ext import commands, tasks
import random
import asyncio
from datetime import datetime, timedelta
from keep_alive import keep_alive

description = '''Isbjorn Support Bot'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_member_join(member):
    welcome_channel = discord.utils.get(member.guild.text_channels, name='welcome')
    if welcome_channel:
        await welcome_channel.send(f'Welcome to the server, {member.mention}! We are glad to have you here. Feel free to ask any questions about polar bear conservation.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'polar bear' in message.content.lower():
        await message.channel.send('Polar bears are fascinating creatures! Did you know that they are classified as marine mammals because they spend most of their lives on the sea ice of the Arctic Ocean?')

    await bot.process_commands(message)

@bot.command()
async def info(ctx):
    await ctx.send('This bot is dedicated to discussing and promoting polar bear conservation. Feel free to ask any questions or share information!')

# Get the token from the environment variable
bot.run(os.getenv("DISCORD_TOKEN"))